from mc_boomer.action import Action, MultiSource 
from search_state import SegmentPolaritySearchState
import initialize
from mc_boomer.util import print_attractors, format_actions

actions = [
# wg
Action(srcs=(MultiSource('CIA', 'i'),MultiSource('SLP', 'i')), dst='wg', type='a'),
Action(srcs=(MultiSource('CIA', 'i'),MultiSource('wg', 'i')), dst='wg', type='a'),
Action(srcs=(MultiSource('SLP', 'i'),MultiSource('wg', 'i')), dst='wg', type='a'),
Action(srcs=(MultiSource('CIR','i'),), dst='wg', type='i'),
# WG
Action(srcs=(MultiSource('wg','i'),), dst='WG', type='a'),
# en
Action(srcs=(MultiSource('WG','e'),), dst='en', type='a'),
Action(srcs=(MultiSource('SLP','i'),), dst='en', type='i'),
# EN
Action(srcs=(MultiSource('en','i'),), dst='EN', type='a'),
# hh
Action(srcs=(MultiSource('EN','i'),), dst='hh', type='a'),
Action(srcs=(MultiSource('CIR','i'),), dst='hh', type='i'),
# HH
Action(srcs=(MultiSource('hh','i'),), dst='HH', type='a'),
# ptc
Action(srcs=(MultiSource('CIA','i'),), dst='ptc', type='a'),
Action(srcs=(MultiSource('EN','i'),), dst='ptc', type='i'),
Action(srcs=(MultiSource('CIR','i'),), dst='ptc', type='i'),
# PTC
Action(srcs=(MultiSource('ptc','i'),), dst='PTC', type='a'),
Action(srcs=(MultiSource('PTC','i'), MultiSource('~HH','e')), dst='PTC', type='a'),

# PH 
Action(srcs=(MultiSource('PTC','i'),MultiSource('HH','e')), dst='PH', type='a'),
# SMO
Action(srcs=(MultiSource('~PTC','i'),), dst='SMO', type='a'),
Action(srcs=(MultiSource('HH','e'),), dst='SMO', type='a'),
# ci
Action(srcs=(MultiSource('EN','i'),), dst='ci', type='i'),
# CI
Action(srcs=(MultiSource('ci','i'),), dst='CI', type='a'),
# CIA
Action(srcs=(MultiSource('CI', 'i'), MultiSource('SMO', 'i')), dst='CIA', type='a'),
Action(srcs=(MultiSource('CI', 'i'), MultiSource('HH', 'e')), dst='CIA', type='a'),
# CIR
Action(srcs=(MultiSource('CI', 'i'),), dst='CIR', type='a'),
Action(srcs=(MultiSource('SMO', 'i'),), dst='CIR', type='i'),
Action(srcs=(MultiSource('HH', 'e'),), dst='CIR', type='i'),
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
