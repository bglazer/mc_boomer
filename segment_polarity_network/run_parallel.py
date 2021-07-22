from mcts import explorationDecay, constantExploration
import random
import json
from datetime import datetime
from joblib import Parallel, delayed
import run

num_steps = int(1e4)
num_jobs = 1500
n_parallel = 35
explorationPolicy = explorationDecay
min_edges = 8
max_edges = 30
keep_tree = True
cache = False
nested = True
threshold = .99


timestamp = datetime.strftime(datetime.now(), format='%Y%m%d-%H%M')
data_dir = './data'


def start(job):
    output_string = f'job-{job}_tmstp-{timestamp}'
    parameter_file = open(f'{data_dir}/parameters/parameters_{output_string}.json','w')
    explorationConstant = random.uniform(.2,.5)
    stop_prior = random.uniform(.6,.9)
    rave_equiv_param = random.randint(1000,500000)
    parameters = {
        'num_steps': num_steps,
        'explorationConstant': explorationConstant,
        'num_jobs': num_jobs,
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
    json.dump(parameters, parameter_file)
    parameter_file.close()

    run.search(stop_prior = stop_prior,
               min_edges = min_edges,
               max_edges = max_edges,
               num_steps = num_steps,
               explorationConstant = explorationConstant,
               explorationPolicy = explorationPolicy,
               rave_equiv_param = rave_equiv_param,
               keep_tree = keep_tree,
               cache = cache,
               nested = nested,
               threshold = threshold,
               stats_file = f'{data_dir}/stats/searchstats_{output_string}.csv',
               model_file = f'{data_dir}/models/models_{output_string}.txt.gz',
               run_file = f'{data_dir}/logs/runlog_{output_string}.log'
              )

parallel = Parallel(n_jobs = n_parallel)
parallel(delayed(start)(i) for i in range(num_jobs))
