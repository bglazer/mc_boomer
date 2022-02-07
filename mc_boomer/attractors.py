from itertools import product
from copy import copy

from scipy.spatial import distance_matrix
from mip import Model, xsum, minimize, CONTINUOUS, OptimizationStatus
from itertools import product
import random
import numpy as np

def pairwise_distance(a,b, penalties=None):
    distances = {}

    a_s = [dict(attr_a) for attr_a in a.keys()]
    b_s = [dict(attr_b) for attr_b in b.keys()]
    for attr_a in a_s:
        for attr_b in b_s:
            d=0
            for node_id in attr_a:
                value_a = attr_a[node_id]
                value_b = attr_b[node_id]
                if penalties:
                    penalty = penalties[node_id]
                else:
                    penalty = 1
                diff = abs(float(value_a - value_b))*penalty
                d += diff
            distances[(tuple(attr_a.items()), tuple(attr_b.items()))] = d
    return distances


def convert_cyclic(attractors):
    combined = dict()

    for cycle, count in attractors.items():    
        len_cycle = len(cycle)
        num_nodes = len(cycle[0])
        squashed = [[key,0] for key,value in cycle[0]]
        for state in cycle:
            for i in range(num_nodes):
                squashed[i][1] += state[i][1]/len_cycle

        squashed = tuple([tuple(pair) for pair in squashed])
        if squashed not in combined:
            combined[squashed] = 0
        combined[squashed] += count

    return combined


def similarity(model, true, verbose=False, penalties=None):
    model = convert_cyclic(model)
    true = convert_cyclic(true)

    adjusted = {attr:0 for attr in true.keys()}
    num_nodes = len(list(model.keys())[0])
    num_attractors = sum(model.values())
    
    if penalties:
        max_distance = sum(penalties.values()) * num_attractors
    else:
        max_distance = num_nodes * num_attractors
    
    edit_distance = 0
    
    distances = pairwise_distance(model, true, penalties)

    sorted_distances = sorted(distances.items(), key=lambda _:_[1])
    for (src, dst), dist in sorted_distances:
        mc = model[src]
        tc = true[dst]
        ac = adjusted[dst]
        c = min(mc, tc-ac)
        if c > 0:
            adjusted[dst] += c
            model[src] -= c
            edit_distance += c*dist

    return 1-edit_distance/max_distance

def distribution_similarity(a, b, sample=None, weighted_sample=False, verbose=False):
    a_states, a_probs = zip(*a.items())
    b_states, b_probs = zip(*b.items())
    n_a = len(a)
    n_b = len(b)
    if sample is not None:
        a_weights = a_probs if weighted_sample else None
        b_weights = b_probs if weighted_sample else None
        a_idx = np.random.choice(len(a), p=a_weights, size=sample, replace=False)
        b_idx = np.random.choice(len(b), p=b_weights, size=sample, replace=False)
        ai = list(a.items())
        bi = list(b.items())
        a = [ai[i] for i in a_idx]
        b = [bi[i] for i in b_idx]
        a_states, a_probs = zip(*a)
        b_states, b_probs = zip(*b)
        a_sum = sum(a_probs)
        b_sum = sum(b_probs)
        a_probs = [p/a_sum for p in a_probs]
        b_probs = [p/b_sum for p in b_probs]
        n_a = n_b = sample

    num_nodes = len(a_states[0])
    
    #D_states = pairwise_distances(a_states, b_states, metric='manhattan')
    D_states = distance_matrix(a_states, b_states, p=1)
   
    model = Model()
    if not verbose:
        model.verbose=0

    variables = []
    for i in range(n_a):
        variables.append(list())
        for j in range(n_b):
            variables[i].append(model.add_var(var_type=CONTINUOUS))
            model += variables[i][j] >= 0
    
    for i in range(n_a):
        # Conserve all of a
        model += xsum(variables[i][j] for j in range(n_b)) == a_probs[i]

    for j in range(n_b):
        # Match b
        model += xsum(variables[i][j] for i in range(n_a)) == b_probs[j]
    

    model.objective = minimize(
        xsum(D_states[i][j]*variables[i][j]
        for i,j in product(range(n_a), range(n_b))))

    
    model.max_gap = 0.0005
    status = model.optimize(max_seconds=300)
    if verbose:
        if status == OptimizationStatus.OPTIMAL:
            print(f'optimal solution cost {model.objective_value} found')
        elif status == OptimizationStatus.FEASIBLE:
            print(f'sol.cost {model.objective_value} found, best possible: {model.objective_bound}')
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print(f'no feasible solution found, lower bound is: {model.objective_bound}')

    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        return 1-model.objective_value/num_nodes
    else:
        return None

def print_attractors(attractors):
    stable, cyclic = attractors

    for attr, count in stable.items():
        for node,value in attr:
            b = 1 if value else 0
            print(b,end='')
        print('|','{:>4}'.format(count))

    for cycle, count in cyclic.items():
        for state in cycle:
            print('')
            for node,value in state:
                b = 1 if value else 0
                print(b,end='')
        print('|','{:>4}'.format(count))

def compare_attractors(a,b):
    for attr in set(list(a.keys()) + list(b.keys())):
        for node,value in attr:
            if value:
                print('1',end=' ')
            else:
                print('0',end=' ')
        ac = a[attr] if attr in a else 0
        bc = b[attr] if attr in b else 0
        print('|','{:>4},{:>4}'.format(ac,bc))
