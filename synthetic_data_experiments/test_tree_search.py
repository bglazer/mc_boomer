from tree_search import run_search
from mcts import explorationDecay, constantExploration
from random import randint
import pickle
import json
from multiprocessing import Pool
from datetime import datetime
import sys
import random


hyperparam_sets = [
                {'nested':True,  'rave':True,  'keep_tree':True},
                {'nested':True,  'rave':True,  'keep_tree':False},
                {'nested':True,  'rave':False, 'keep_tree':True},
                {'nested':True,  'rave':False, 'keep_tree':False},
                {'nested':False, 'rave':True,  'keep_tree':True},
                {'nested':False, 'rave':True,  'keep_tree':False},
                {'nested':False, 'rave':False, 'keep_tree':True},
                {'nested':False, 'rave':False, 'keep_tree':False}
              ]

num_repeats = 10
# These were chosen semi-empirically by looking at the max/min
# number of interactions in the sampled graphs
min_edges = {8:8,  16:16,  32:32} 
max_edges = {8:40, 16:120, 32:496}

# Previous experiments showed that only a tiny fraction of cached models were re-hit
# and that the memory cost was too high for the value
cache = False

data_dir = '/home/bglaze/deepgraph/data' 
data_timestamp = '20201215_123542'
current_timestamp = datetime.strftime(datetime.now(), format='%Y%m%d-%H%M')

def run(parameters, i,j, nodes, true_attractors, start_states):
    num_nodes = parameters['num_nodes']
    model_idx = parameters['model_idx']
    stop_prior = parameters['stop_prior']
    min_edges = parameters['min_edges']
    max_edges = parameters['max_edges']
    num_steps = parameters['num_steps']
    explorationConstant = parameters['explorationConstant']
    rave_equiv_param = parameters['rave_equiv_param']
    keep_tree = parameters['keep_tree']
    cache = parameters['cache']
    nested = parameters['nested']
    model_idx = parameters['model_idx']
    model_idx = parameters['model_idx']

    output_string = f'numnodes-{num_nodes}_process-{i}_repeat-{j}_tmstp-{current_timestamp}'

    run_search(nodes,
               true_attractors,
               start_states = start_states,
               stop_prior = stop_prior,
               min_edges = min_edges,
               max_edges = max_edges,
               num_steps = num_steps,
               explorationConstant = explorationConstant,
               # NOTE this is hardcoded
               explorationPolicy = explorationDecay,
               rave_equiv_param = rave_equiv_param,
               keep_tree = keep_tree,
               cache = cache,
               nested = nested,
               stats_file = f'{data_dir}/stats/search_stats-{output_string}.csv',
               model_file = f'{data_dir}/models/models-{output_string}.txt.gz',
               run_file = f'{data_dir}/logs/run_log-{output_string}.log'
              )

pool = Pool(processes=30)
processes = []

for num_nodes in [8, 16, 32]:
    nodes = list(range(num_nodes))
    models = pickle.load(open(f'{data_dir}/inputs/models_sync_{num_nodes}_{data_timestamp}.pickle','rb'))
    attractors = pickle.load(open(f'{data_dir}/inputs/attractors_sync_{num_nodes}_{data_timestamp}.pickle','rb'))
    #TODO need to adapt boolan model to accept predefeined starting states
    start_states = pickle.load(open(f'{data_dir}/inputs/start_states_sync_{num_nodes}_{data_timestamp}.pickle','rb'))

    for hyperparam_idx, hyperparams in enumerate(hyperparam_sets):
        num_steps = int(1e4)
        explorationPolicy = explorationDecay
        keep_tree = hyperparams['keep_tree']
        nested = hyperparams['nested']
        explorationConstant = tuple([random.uniform(.2,.5) for i in range(num_repeats)])
        stop_prior = tuple([random.uniform(.2,.7) for i in range(num_repeats)])
        if hyperparams['rave']:
            rave_equiv_param = tuple([random.randint(1000,500000) for i in range(num_repeats)])
        else:
            rave_equiv_param = tuple([None for i in range(num_repeats)])

        for repeat_idx in range(num_repeats):
            model_idx = randint(0, len(models[num_nodes])-1)

            true_stable_attractors = attractors[num_nodes][0][model_idx]
            true_cyclic_attractors = attractors[num_nodes][1][model_idx]
            true_attractors = (true_stable_attractors, true_cyclic_attractors)

            parameters = {
                'setting': 'deepgraph parameter and performance experiments',
                'num_nodes': num_nodes,
                'model_idx': model_idx,
                'num_steps': num_steps,
                'explorationConstant': explorationConstant[repeat_idx],
                'min_edges': min_edges[num_nodes],
                'max_edges': max_edges[num_nodes],
                'explorationPolicy': explorationPolicy.__name__,
                'stop_prior': stop_prior[repeat_idx],
                'rave_equiv_param': rave_equiv_param[repeat_idx],
                'keep_tree': keep_tree,
                'cache': cache,
                'nested': nested,
                'model_idx':model_idx
            }

            # TODO remove slurm add process index
            output_string = f'numnodes-{num_nodes}_process-{hyperparam_idx}_repeat-{repeat_idx}_tmstp-{current_timestamp}'
            parameter_file = open(f'{data_dir}/parameters/parameters-{output_string}.json','w')
            json.dump(parameters, parameter_file)
            parameter_file.close()

            print(f'starting hyperparams {hyperparam_idx}, repeat {repeat_idx}', flush=True)
            process = pool.apply_async(func=run, args=(parameters, hyperparam_idx, repeat_idx, nodes, true_attractors, start_states[num_nodes][model_idx]))
            #run(hyperparam_idx, repeat_idx, nodes, true_attractors, start_states[num_nodes][model_idx])
            processes.append(process)

for i,process in enumerate(processes):
    process.wait()
    print(f'{i} processes done')

