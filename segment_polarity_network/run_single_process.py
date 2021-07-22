from mc_boomer.mcts import explorationDecay, constantExploration
import json
from datetime import datetime
import random
import run

#num_steps = int(5e4)
num_steps = int(10)
num_processes = 1
explorationPolicy = explorationDecay
min_edges = 8
max_edges = 30
explorationConstant = tuple([random.uniform(.2,.5) for i in range(num_processes)])
stop_prior = tuple([random.uniform(.6,.9) for i in range(num_processes)])
rave_equiv_param = tuple([random.randint(1000,500000) for i in range(num_processes)])
#rave_equiv_param = tuple([None for i in range(num_processes)])
keep_tree = True
cache = False
nested = True
threshold = .99

parameters = {
    'num_steps': num_steps,
    'explorationConstant': explorationConstant,
    'num_processes': num_processes,
    'min_edges': min_edges,
    'max_edges': max_edges,
    'explorationPolicy': explorationPolicy.__name__,
    'stop_prior': stop_prior,
    'rave_equiv_param': rave_equiv_param,
    'keep_tree': keep_tree,
    'cache': cache,
    'nested': nested,
    'experiments': True,
    'reward':'avg',
    'threshold':threshold
}

timestamp = datetime.strftime(datetime.now(), format='%Y%m%d-%H%M')
data_dir = './data'


def start(job):
    parameter_file = open(f'{data_dir}/parameters/parameters-job-{job}.json','w')
    json.dump(parameters, parameter_file)
    parameter_file.close()

    output_string = f'job-{job}_tmstp-{timestamp}'
    run.search(stop_prior = stop_prior[job],
               min_edges = min_edges,
               max_edges = max_edges,
               num_steps = num_steps,
               explorationConstant = explorationConstant[job],
               explorationPolicy = explorationPolicy,
               rave_equiv_param = rave_equiv_param[job],
               keep_tree = keep_tree,
               cache = cache,
               nested = nested,
               threshold=threshold,
               stats_file = f'{data_dir}/stats/search_stats-{output_string}.csv',
               model_file = f'{data_dir}/models/models-{output_string}.txt.gz',
               run_file = f'{data_dir}/logs/run_log-{output_string}.log'
              )
start(0)
