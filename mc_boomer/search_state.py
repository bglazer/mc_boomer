from copy import copy
import mc_boomer.attractors
from mc_boomer.action import Action

class SearchState():
    def __init__(self, model, data_attractors, start_states, stop_prior=0.0, min_edges=0, max_edges=0, actions=None, num_edges=0):
        self.model = model
        self.data_attractors = data_attractors
        self.start_states = start_states
        self.stop_prior = stop_prior
        self.max_edges = max_edges
        self.min_edges = min_edges
        self.stopped = False
        self.num_edges = num_edges

        self.actions = actions
    

    def __copy__(self):
        newstate = SearchState(copy(self.model),
                               self.data_attractors,
                               self.start_states,
                               self.stop_prior,
                               self.min_edges, self.max_edges, actions=copy(self.actions),
                               num_edges = self.num_edges)
        return newstate
        
    #Returns an iterable of all actions which can be taken from this state
    def getPossibleActions(self): 
        return list(self.actions.items())
    
    #Returns the state which results from taking action 
    def takeAction(self, action, compile=True): 
        newstate = copy(self)
        
        # the action has two parts, the first defines the action to take, adding an edge, etc.
        # the second part is the prior probability of taking that action, 

        if action == ('stop'):
            newstate.stopped = True
            return newstate
            
        newstate.model.add(action)
        if compile:
            newstate.model.compile_rules()

        # Update the actions available for the next step, we don't want to be able to 
        # add the same edge twice, or have an inhibiting and activating edge from the
        # same source
        inhib = Action(srcs=action.srcs, dst=action.dst, type='i')
        activ = Action(srcs=action.srcs, dst=action.dst, type='a')
        if activ in newstate.actions:
            del newstate.actions[activ]
        if inhib in newstate.actions:
            del newstate.actions[inhib]

        # update the prior probabilities of choosing each action. Sums to 1
        # The stop action has a fixed prior once we pass the minimum number of edges
        # TODO variable prior depending on number of edges
        if self.num_edges > self.min_edges:
            newstate.actions[('stop')] = self.stop_prior

        normalization = sum(newstate.actions.values())
        # normalize the priors
        for action in newstate.actions:
            newstate.actions[action] = newstate.actions[action]/normalization

        newstate.num_edges += 1
        
        return newstate


    #Returns whether this state is a terminal state
    def isTerminal(self):
        if self.stopped:
            return True
        if self.num_edges > self.max_edges:
            return True
        return False

    #Returns the reward for this state. Only needed for terminal states.
    def getReward(self): 
        if self.start_states is None:
            simulated_attractors = self.model.simulate_all()
        else:
            simulated_attractors = self.model.simulate(self.start_states)

        similarity = attractors.similarity(simulated_attractors, self.data_attractors)
        return similarity

    # Needed for the MCTS heapq. If sort keys are equal, then heapq defaults to sorting by value,
    # so we have to define a placeholder comparison operator
    def __lt__(self, b):
        return True
