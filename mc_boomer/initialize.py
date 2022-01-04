from itertools import permutations, product
from mc_boomer.action import Action, Source
from mc_boomer.boolean_model import BooleanModel


def emptyModel(nodes):
    # Create a node copy for every cell 
    rules = {}
    for node in nodes:
        rules[node] = ([],[])

    # initialize empty model
    model = BooleanModel(rules=rules)
    return model
    
# TODO adding actions according to interaction graph
# TODO removing/adding actions from prior knowledge -> i.e. manually encoded actions
def allActions(model, interaction_graph=None, prior_knowledge=None):
    interactions = list(product(model.nodes, model.nodes))
    actions = []

    for src,dst in interactions:
        actions.append(Action(srcs=(src,), type='a', dst=dst))
        actions.append(Action(srcs=(src,), type='i', dst=dst))

    return actions

# TODO custom prior
def addPrior(actions, stop=False, custom_prior=None):
    prior = 1/(len(actions))
    ax = {action: prior for action in actions}
    if stop:
        ax['stop'] = 0.0
    return ax

# TODO initialize with known interactions
def initialState(known_actions=None):
    model = emptyModel()

    actions = allActions()

    return model, addPrior(list(actions))
