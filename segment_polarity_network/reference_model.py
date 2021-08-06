from mc_boomer.action import Action, Source 
from search_state import SegmentPolaritySearchState
import initialize
from mc_boomer.util import print_attractors, format_actions

actions = [
# wg
Action(srcs=(Source('CIA', 'i'),Source('SLP', 'i')), dst='wg', type='a'),
Action(srcs=(Source('CIA', 'i'),Source('wg', 'i')), dst='wg', type='a'),
Action(srcs=(Source('SLP', 'i'),Source('wg', 'i')), dst='wg', type='a'),
Action(srcs=(Source('CIR','i'),), dst='wg', type='i'),
# WG
Action(srcs=(Source('wg','i'),), dst='WG', type='a'),
# en
Action(srcs=(Source('WG','e'),), dst='en', type='a'),
Action(srcs=(Source('SLP','i'),), dst='en', type='i'),
# EN
Action(srcs=(Source('en','i'),), dst='EN', type='a'),
# hh
Action(srcs=(Source('EN','i'),), dst='hh', type='a'),
Action(srcs=(Source('CIR','i'),), dst='hh', type='i'),
# HH
Action(srcs=(Source('hh','i'),), dst='HH', type='a'),
# ptc
Action(srcs=(Source('CIA','i'),), dst='ptc', type='a'),
Action(srcs=(Source('EN','i'),), dst='ptc', type='i'),
Action(srcs=(Source('CIR','i'),), dst='ptc', type='i'),
# PTC
Action(srcs=(Source('ptc','i'),), dst='PTC', type='a'),
Action(srcs=(Source('PTC','i'), Source('~HH','e')), dst='PTC', type='a'),

# PH 
Action(srcs=(Source('PTC','i'),Source('HH','e')), dst='PH', type='a'),
# SMO
Action(srcs=(Source('~PTC','i'),), dst='SMO', type='a'),
Action(srcs=(Source('HH','e'),), dst='SMO', type='a'),
# ci
Action(srcs=(Source('EN','i'),), dst='ci', type='i'),
# CI
Action(srcs=(Source('ci','i'),), dst='CI', type='a'),
# CIA
Action(srcs=(Source('CI', 'i'), Source('SMO', 'i')), dst='CIA', type='a'),
Action(srcs=(Source('CI', 'i'), Source('HH', 'e')), dst='CIA', type='a'),
# CIR
Action(srcs=(Source('CI', 'i'),), dst='CIR', type='a'),
Action(srcs=(Source('SMO', 'i'),), dst='CIR', type='i'),
Action(srcs=(Source('HH', 'e'),), dst='CIR', type='i'),
]


if __name__ == '__main__':
    spm = initialize.emptyModel()
    for action in actions:
        spm.add(action)

    spm.compile_rules(verbose=True)
    #spm.compile_rules(verbose=False)
        
    state = SegmentPolaritySearchState(spm)
    attractors = state.getAttractors()
    state.printAttractors(attractors)
    #
    reward = state.getReward()
    print(f'Similarity: {reward:.4f}')

    print(f'Similarity reduction')
    for i in range(len(actions)):
        one_out_actions = actions.copy()
        one_out_actions.pop(i)
        spm = initialize.emptyModel()
        for action in one_out_actions:
            spm.add(action)
       
        spm.compile_rules(verbose=False)
            
        state = SegmentPolaritySearchState(spm)
        
        reward = state.getReward()
        print(f'{1-reward:6.4f}', end=' ')
        format_actions([actions[i]])
