#!/usr/bin/env python
# coding: utf-8

from boolean_model import BooleanModel
import random
from math import log
import pickle
import initialize 
from joblib import Parallel, delayed
from datetime import datetime
import sys
from action import Action


def random_actions_model(num_nodes, p_action, self_loops=False, verbose=False):
    nodes = [str(i) for i in range(num_nodes)]
    model = initialize.emptyModel(nodes = nodes)
    actions = initialize.allActions(nodes=nodes)
    actions = initialize.addPrior(actions)

    num_activ =0
    num_inhib = 0
    added = []
    while len(actions) > 0:
        p = random.random()
        action = random.sample(actions.keys(), k=1)[0]
        if p > p_action:
            del actions[action]
        else:
            if action == 'stop':
                continue
            num_activ += 1 if action.type == 'a' else 0
            num_inhib += 1 if action.type == 'i' else 0

            added.append(action)
            model.add(action)
            del actions[action]
            opposite_type = Action(srcs=action.srcs, dst=action.dst, type='i' if action.type == 'a' else 'a')
            if opposite_type in actions:
                del actions[opposite_type]
            
    if verbose:
        print(f'num_actions: {num_activ+num_inhib}, num_inhib: {num_inhib}, num_activ: {num_activ}')
    return model, added

def shift(x, stop, start):
    return start + (stop-start)*x

def sample(num_nodes, verbose=False):
    min_p_action = .01
    max_p_action = .6
    p_action = shift(random.random(), min_p_action, max_p_action)
    if verbose:
        print(p_action)
    model,actions = random_actions_model(num_nodes, p_action)
    return model, actions

def simulate_async(model, num_starts, num_steps):
    state_probabilities = model.simulate_async(num_starts, num_steps)
    return model, state_probabilities

def simulate_sync(model, num_starts):
    # Probability used to generate start state
    # for each node, if random > prob_true_state, then node=True 
    # shift to ensure we don't get a random p that is very high or very low
    # thus making it difficult to generate enough unique starting states
    prob_true_state = shift(random.random(), .2, .8)
    starts, attractors = model.simulate_random(num_starts=num_starts, p=prob_true_state)
    return starts, attractors

def sample_simulate_sync(num_nodes, num_starts, verbose=False):
    variety_rules = [
        lambda n_stable, n_cyclic: n_stable > 1,
        lambda n_stable, n_cyclic: n_stable > 2,
        lambda n_stable, n_cyclic: n_stable > 3,
        lambda n_stable, n_cyclic: n_cyclic > 1 and n_cyclic < 10,
        lambda n_stable, n_cyclic: n_cyclic > 2 and n_cyclic < 10,
        lambda n_stable, n_cyclic: n_cyclic > 3 and n_cyclic < 10,
        lambda n_stable, n_cyclic: n_stable < 4 and n_cyclic == 0,
        lambda n_stable, n_cyclic: n_stable < 5 and n_cyclic == 0,
        lambda n_stable, n_cyclic: n_stable < 6 and n_cyclic == 0,
        ]
    
    variety_rule = random.choice(variety_rules)

    i = 0
    variety = False
    while not variety:
        model,actions = sample(num_nodes, verbose)
        starts, attractors = simulate_sync(model, num_starts)
        nstable = len([None for attractor in attractors if len(attractor)==1])
        ncycles = len([None for attractor in attractors if len(attractor)>1])
        if verbose:
            print(nstable, ncycles)
        variety = variety_rule(nstable, ncycles)
        i += 1
        
    return actions, starts, attractors
    
def sample_simulate_async(num_nodes, num_starts, num_steps):
    # zero one balance
    zb = 0.0
    # entropy
    e = 0.0
    connected = False
    model = None
    while zb < .25 or zb > .75 or e < 1.0 or not connected:
        model = sample(num_nodes)
        # TODO make sure this is correct before running!
        model, state_probabilities = simulate_async(model, num_starts, num_steps)
        zb = zero_one_balance(state_probabilities)
        e = entropy(state_probabilities)
        connected = nx.components.is_weakly_connected(model.graph)
    return model, state_probabilities


def entropy(distribution):
    e = 0
    for state,prob in distribution.items():
        e -= prob * log(prob)
    return e

def zero_one_balance(distribution):
    p = 0
    for state, prob in distribution.items():
        p+=sum(state)/len(state)*prob
    return p


if __name__ == '__main__':
    if sys.argv[1] == 'sync':
        #num_nodes_list = [8, 16]
        #num_starts_list = [100, 1000]
        num_nodes_list = [32]
        num_starts_list = [10000]

        params = zip(num_nodes_list, num_starts_list)

        parallel = Parallel(n_jobs=30, verbose=10)

        total_models = 100

        tmstp = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
        datadir = '/home/bglaze/deepgraph/data/inputs'
        print(tmstp)

        #all_models = {}
        all_actions = {}
        all_attractors = {}
        all_start_states = {}
        for num_nodes, num_starts in params:
            print('start',num_nodes,datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            results = parallel(delayed(sample_simulate_sync)(num_nodes, num_starts, verbose=True) for i in range(total_models))
            #results = [sample_simulate_sync(num_nodes, num_starts) for i in range(total_models)]

            actions, start_states, attractors = zip(*results)
            #all_models[num_nodes] = models
            all_actions[num_nodes] = actions
            all_start_states[num_nodes] = start_states
            all_attractors[num_nodes] = attractors
            print('end',num_nodes,datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))

        #pickle.dump(all_models, open(f'{datadir}/models_sync_{num_nodes}_{tmstp}.pickle','wb'))
        pickle.dump(all_actions, open(f'{datadir}/actions_sync_{tmstp}.pickle','wb'))
        pickle.dump(all_attractors, open(f'{datadir}/attractors_sync_{tmstp}.pickle','wb'))
        pickle.dump(all_start_states, open(f'{datadir}/start_states_sync_{tmstp}.pickle','wb'))

    elif sys.argv[1] == 'async':
        num_nodes_list = [8]
        # TODO change these params
        num_steps_list = [250]
        num_starts_list = [170]

        params = zip(num_nodes_list, num_steps_list, num_starts_list)

        all_models = {}
        all_state_probabilities = {}
        parallel = Parallel(n_jobs=100, verbose=10)

        total_models = 100

        for num_nodes, num_steps, num_starts in params:
            results = parallel(delayed(sample_simulate)(num_nodes, num_starts, num_steps) for i in range(total_models))

            models, state_probabilities = zip(*results)
            all_models[num_nodes] = models
            all_state_probabilities[num_nodes] = state_probabilities

        from datetime import datetime
        tmstp = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
        datadir = '/data/lola/glazerb/deepgraph'
        print(tmstp)
        pickle.dump(all_models, open(f'{datadir}/models_{tmstp}.pickle','wb'))
        pickle.dump(all_state_probabilities, open(f'{datadir}/state_probabilities_{tmstp}.pickle','wb'))

    else:
        print('must provide "sync" or "async" as arguments to script')

