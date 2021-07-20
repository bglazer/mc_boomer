from collections import Counter
from functools import reduce
from itertools import combinations, product
from mc_boomer.util import action_set
from mc_boomer.search_state import add_to_rules
import mc_boomer.initialize 

def common(models, order=[1], verbose=False, excluded=set()):
    if type(order) is not list:
        raise Exception(f'order argument must be a list, you passed: {type(order)}')
    if type(excluded) is not set:
        raise Exception(f'excluded argument must be a set, you passed: {type(excluded)}')

    actions = Counter()
    
    count=0
    n_models = len(models)
    step = int(n_models/10)
    step = 1 if step == 0 else step

    for model in models:
        if verbose:
            count+=1
            if count % step == 0:
                print(f'common analysis progress: {count/len(models)*100:.0f}%')

        actionset = action_set(model) - excluded
                    
        for i in order:
            # Higher order interactions. i.e. pairs, triples.. of interactions
            combos = combinations(actionset, r=i)

            for combo in combos:
                actions[combo] += 1/n_models

    return actions


def superset_filter(common_differences):
    # prevent inclusion of higher order interactions that are just super-sets 
    # of an already included interaction
    filtered = dict()

    interaction_sets = [(set(interaction),percent) for interaction,percent in common_differences.items()]
    for interaction, percent in sorted(interaction_sets, key=lambda _: len(_[0])):
        isnew = True
        for prev_interaction, _ in interaction_sets:
            if len(prev_interaction) == len(interaction):
                break
            if prev_interaction.issubset(interaction):
                isnew = False
                break
        if isnew:
            filtered[tuple(interaction)] = percent

    return filtered

def unique(clusters, uniqueness_threshold, order, verbose=False, excluded=set()):
    interactions = {}
    for cluster,models in clusters.items():
        if verbose:
            print(f'Common analysis cluster: {cluster}')
        interactions[cluster] = common(models, order, verbose=verbose, excluded=excluded)

    differences = {cluster:Counter() for cluster in interactions}

    num_comparisons = len(interactions)-1
    # All pairs of clusters
    if verbose:
        print('Calculating differences')

    # TODO change to product
    for cluster1, cluster2 in product(interactions.keys(), interactions.keys()):
        # Interactions that are present in all models in that cluster
        one = interactions[cluster1].items()
        two = interactions[cluster2]
        for inter, pct1 in one:
            if inter in two:
                pct2 = two[inter]
            else:
                pct2 = 0.0
            diff = pct1 - pct2
            differences[cluster1][inter] += diff/num_comparisons

    if verbose:
        print('Calculating Uniqueness')

    # Filter interactions that are unique at a given percentage level
    # i.e. find the most "distinguishing" interactions
    common_differences = {cluster:dict() for cluster in differences}
    for cluster in differences:
        # add the shortest (lowest order) interactions first
        for interaction, percent in differences[cluster].items():
            if percent >= uniqueness_threshold:
                common_differences[cluster][interaction] = percent

    return common_differences
