from mc_boomer.action import Action, Source
import initialize
from mc_boomer.util import print_attractors, format_actions

actions = [
#Action(srcs=(Source('a'),Source('b',neg=False)), dst='c', type='a'),
Action(srcs=(Source('a'),), dst='c', type='a'),
#Action(srcs=(Source('b'),), dst='c', type='a'),
#Action(srcs=(Source('b',neg=False),), dst='c', type='i'),
]


if __name__ == '__main__':
    model = initialize.emptyModel(nodes=['a','b','c'])
    for action in actions:
        model.add(action)
    
    model.state = {'a':False, 'b':False, 'c':False}
    print('00',model.update(node='c'))
    model.state = {'a':False, 'b':True,  'c':False}
    print('01',model.update(node='c'))
    model.state = {'a':True,  'b':False, 'c':False}
    print('10',model.update(node='c'))
    model.state = {'a':True,  'b':True,  'c':False}
    print('11',model.update(node='c'))
