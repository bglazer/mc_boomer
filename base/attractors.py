from itertools import product, permutations
from copy import deepcopy, copy
from fractions import Fraction

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
    stable, cycles = attractors
    combined = dict()

    for cycle, count in cycles.items():    
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

    for state, count in stable.items():
        combined[state] = count
    
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
