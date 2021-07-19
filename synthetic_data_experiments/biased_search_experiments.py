from tree_search import SearchState
import run
import initialize
from boolean_model import BooleanModel
from mcts import explorationDecay, constantExploration
import pickle
import json
from multiprocessing import Pool
from datetime import datetime
import random
import math

def start(boolean_model_state, parameters, output_string):
    run.search(boolean_model_state,
               min_edges = parameters['min_edges'],
               max_edges = parameters['max_edges'],
               num_steps = parameters['num_steps'],
               explorationConstant = parameters['explorationConstant'],
               # NOTE this is hardcoded
               explorationPolicy = explorationDecay,
               rave_equiv_param = parameters['rave_equiv_param'],
               keep_tree = parameters['keep_tree'],
               cache = parameters['cache'],
               nested = parameters['nested'],
               threshold = parameters['threshold'],
               stats_file = f'{data_dir}/stats/search_stats-{output_string}.csv',
               model_file = f'{data_dir}/models/models-{output_string}.txt.gz',
               run_file = f'{data_dir}/logs/run_log-{output_string}.log'
              )


num_repeats = 5
num_steps = int(1e4)
# These were chosen semi-empirically by looking at the max/min
# number of interactions in the sampled graphs
min_edges = {8:8,  16:16,  32:32} 
max_edges = {8:40, 16:120, 32:496}

# Previous experiments showed that only a tiny fraction of cached models were re-hit
# and that the memory cost was too high for the value
cache = False

data_dir = '/home/bglaze/deepgraph/data' 
data_timestamp = '20210614_112716'
current_timestamp = datetime.strftime(datetime.now(), format='%Y%m%d-%H%M')

pool = Pool(processes=30)
processes = []

percent_action_experiments = [.9, .75, .5, .25, .1]
threshold = 0.0

#for num_nodes in [8, 16]:
for num_nodes in [32]:
    nodes = [str(x) for x in range(num_nodes)]
    default_actions = initialize.allActions(nodes)
    bm = initialize.emptyModel(nodes)

    actions = pickle.load(open(f'{data_dir}/inputs/actions_sync_{data_timestamp}.pickle','rb'))
    attractors = pickle.load(open(f'{data_dir}/inputs/attractors_sync_{data_timestamp}.pickle','rb'))
    start_states = pickle.load(open(f'{data_dir}/inputs/start_states_sync_{data_timestamp}.pickle','rb'))

    # TODO Do we need repeats, if so, how many??
    for repeat_idx in range(num_repeats):
        explorationPolicy = explorationDecay
        # Based on good results from previous experiments, we turn RAVE, tree retention (keep_tree), and nested search on
        keep_tree = True
        nested = True
        rave_equiv_param = tuple([random.randint(1000,500000) for i in range(num_repeats)])

        explorationConstant = tuple([random.uniform(.2,.5) for i in range(num_repeats)])
        stop_prior = tuple([random.uniform(.2,.7) for i in range(num_repeats)])

        model_idx = random.randint(0, len(actions[num_nodes])-1)

        true_actions = actions[num_nodes][model_idx]
        true_attractors = attractors[num_nodes][model_idx]

        for hyperparam_idx, percent_actions in enumerate(percent_action_experiments):
            parameters = {
                'setting': 'synthetic data biased search experiments',
                'percent_actions': percent_actions,
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
                'threshold': threshold,
                'repeat_idx': repeat_idx,
                'hyperparam_idx': hyperparam_idx
            }

            # Add the actions in the true model to the action set
            # This ensures that we can actually recreate the true model
            possible_actions = set(default_actions)
            biased_actions = set()
            for action in true_actions:
                biased_actions.add(action)
                possible_actions.remove(action)

            # Select a random subset of other actions to make the action list 
            # length equal to the predefined size
            n_biased_actions = math.ceil(len(possible_actions)*percent_actions)
            print(len(default_actions), len(possible_actions), len(biased_actions), n_biased_actions)
            random_actions = random.sample(possible_actions, k=n_biased_actions)
            for action in random_actions:
                biased_actions.add(action)

            n_actions = len(biased_actions)
            # TODO change this for "true" actions
            prior = .5 * (1./n_actions)
            biased_actions = {action:prior for action in biased_actions}

            boolean_model_state = SearchState(bm, 
                                              true_attractors, 
                                              start_states=start_states[num_nodes][model_idx], 
                                              min_edges=min_edges[num_nodes], 
                                              max_edges=max_edges[num_nodes],
                                              actions=biased_actions)

            output_string = f'bias_experiment_numnodes-{num_nodes}_process-{hyperparam_idx}_repeat-{repeat_idx}_tmstp-{current_timestamp}'
            parameter_file = open(f'{data_dir}/parameters/parameters-{output_string}.json','w')
            json.dump(parameters, parameter_file)
            parameter_file.close()

            print(f'Starting hyperparams {hyperparam_idx}, repeat {repeat_idx}, percent {percent_actions}', flush=True)
            #start(boolean_model_state,
            #      parameters,
            #      output_string)
            args = (boolean_model_state, 
                    parameters,
                    output_string)
            process = pool.apply_async(func=start, args=args)
            processes.append(process)
            print(process)

for i,process in enumerate(processes):
    process.wait()
    print(f'{i} processes done, success: {process.successful()}')
