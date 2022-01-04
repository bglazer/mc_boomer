from reference_model import actions

from mc_boomer.action import Action, MultiSource 
from search_state import SegmentPolaritySearchState
import initialize
from util import print_async_attractors

import random


if __name__ == '__main__':
    spm = initialize.emptyModel()
    for action in actions:
        spm.add(action)

    start_states = []
    n_states = 10000
    for i in range(n_states):
        p = random.random()
        start_state = {node: random.random() > .5 for node in spm.nodes}
        start_states.append((start_state, 1/n_states))

    num_starts = 100
    num_steps = 50

    state_probs = spm.simulate_async(start_states, num_starts, num_steps)
    print_async_attractors(sorted(state_probs.items(), key=lambda x:x[1]))
    
    
