from reference_model import actions

from mc_boomer.action import Action, MultiSource 
from search_state import SegmentPolaritySearchState
import initialize
from util import print_async_attractors
from attractor_data import wild_type_initial

import random


if __name__ == '__main__':
    spm = initialize.emptyModel()

    for action in actions:
        spm.add(action)

    spm.compile_rules(verbose=True)

    start_states = []
    #for i in range(n_states):
    #    p = random.random()
    #    start_state = {node: random.random() > .5 for node in spm.nodes}
    #    start_states.append((start_state, 1/n_states))

    start_states = [(wild_type_initial[0], 1.0)]

    num_starts = 100000
    num_steps = 50

    state_probs = spm.simulate_async(start_states, num_starts, num_steps)
    #print_async_attractors(sorted(state_probs.items(), key=lambda x:x[1]))
    
    
