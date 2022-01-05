import pickle
from copy import copy
from mc_boomer import attractors 
from attractor_data import en_overexpression, hh_overexpression, initial_perturb_true_attractors, knockout_true_attractors, wild_type_initial, wild_type_true_attractors
from mc_boomer.action import Action
from util import print_attractors
from mc_boomer.search_state import SearchState

def knockout(model, knockout_nodes):
    model = copy(model)
    for knockout_node in knockout_nodes:
        for cell_idx in range(model.num_cells):
            ko = (knockout_node,cell_idx)
            model.rules[ko] = ([],[])
            for node in model.rules.keys():
                activ, inhib = model.rules[node]
                if ko in activ:
                    activ.remove(ko)
                if ko in inhib:
                    inhib.remove(ko)
                model.rules[node] = (activ, inhib)
    return model

class SegmentPolaritySearchState(SearchState):
    def __init__(self, model, stop_prior=0.0, min_edges=0, max_edges=0, actions=None, num_edges=0):
        self.model = model 
        self.stop_prior = stop_prior
        self.max_edges = max_edges
        self.min_edges = min_edges
        self.stopped = False
        self.num_edges = num_edges

        self.actions = actions
    

    def __copy__(self):
        newstate = SegmentPolaritySearchState(copy(self.model),
                                              self.stop_prior,
                                              self.min_edges,
                                              self.max_edges,
                                              actions=copy(self.actions),
                                              num_edges = self.num_edges)
        return newstate

    
    def printAttractors(self, attractors):
        (wild_type_attractors,
         #hh_initial_perturb_attractors,
         #en_initial_perturb_attractors,
         wg_knockout_attractors,
         en_knockout_attractors,
         hh_knockout_attractors
         ) = attractors

        print('')
        print('Wild Type')
        print_attractors(wild_type_attractors, wild_type_true_attractors, squashed=False)
        #print('')
        #print('hh Perturbation')
        #print_attractors(hh_initial_perturb_attractors, initial_perturb_true_attractors, squashed=False)
        #print('')
        #print('en Perturbations')
        #print_attractors(en_initial_perturb_attractors, initial_perturb_true_attractors, squashed=False)
        print('')
        print('wg Knockout')
        print_attractors(wg_knockout_attractors, knockout_true_attractors, squashed=False)
        print('')
        print('en Knockout')
        print_attractors(en_knockout_attractors, knockout_true_attractors, squashed=False)
        print('')
        print('hh Knockout')
        print_attractors(hh_knockout_attractors, knockout_true_attractors, squashed=False)
        print('')
        print('\\newpage')

    def getAttractors(self):
        wild_type_attractors = self.model.simulate(wild_type_initial, fresh_compile=True)

        # hh overexpression experiment
        #hh_initial_perturb_attractors = self.model.simulate(hh_overexpression, fresh_compile=False)

        # en overexpression experiment
        #en_initial_perturb_attractors = self.model.simulate(en_overexpression, fresh_compile=False)
        
        # wg knockout
        wg_knockout_model = knockout(self.model, ['wg', 'WG'])
        wg_knockout_attractors = wg_knockout_model.simulate(wild_type_initial, fresh_compile=True)

        # en knockout
        en_knockout_model = knockout(self.model, ['en', 'EN'])
        en_knockout_attractors = en_knockout_model.simulate(wild_type_initial, fresh_compile=True)

        # hh knockout
        hh_knockout_model = knockout(self.model, ['hh', 'HH'])
        hh_knockout_attractors = hh_knockout_model.simulate(wild_type_initial, fresh_compile=True)

        attractors = (wild_type_attractors,
                      #hh_initial_perturb_attractors,
                      #en_initial_perturb_attractors,
                      wg_knockout_attractors,
                      en_knockout_attractors,
                      hh_knockout_attractors)
        return attractors
        
    def getScores(self, results): 
        (wild_type_attractors,
         #hh_initial_perturb_attractors,
         #en_initial_perturb_attractors,
         wg_knockout_attractors,
         en_knockout_attractors,
         hh_knockout_attractors
         ) = results

        # Score the similarity of results
        wild_type_score = attractors.similarity(wild_type_attractors, wild_type_true_attractors)

        # hh overexpression experiment
        #hh_initial_perturb_score = attractors.similarity(hh_initial_perturb_attractors, initial_perturb_true_attractors)

        # en overexpression experiment
        #en_initial_perturb_score = attractors.similarity(en_initial_perturb_attractors, initial_perturb_true_attractors)

        # wg knockout
        wg_knockout_score = attractors.similarity(wg_knockout_attractors, knockout_true_attractors)

        # en knockout
        en_knockout_score = attractors.similarity(en_knockout_attractors, knockout_true_attractors)

        # hh knockout
        hh_knockout_score = attractors.similarity(hh_knockout_attractors, knockout_true_attractors)

        scores = (wild_type_score, 
                  #hh_initial_perturb_score,
                  #en_initial_perturb_score,
                  wg_knockout_score,
                  en_knockout_score,
                  hh_knockout_score)
        return scores

    # Returns the reward for this state. Only needed for terminal states.
    # TODO this uses an average to combine the rewards from individual experiments
    #  other options include min score or weighted average.
    def getReward(self):
        attractors = self.getAttractors()
        scores = self.getScores(attractors)
        return sum(scores)/len(scores)

    # Needed for the MCTS heapq. If sort keys are equal, then heapq defaults to sorting by value,
    # so we have to define a placeholder comparison operator
    def __lt__(self, b):
        return True
        

