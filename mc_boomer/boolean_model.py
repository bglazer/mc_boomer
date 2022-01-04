from collections import defaultdict
from itertools import product
from copy import copy
import random
from mc_boomer.util import bool_state, to_int, rotate_list
from mc_boomer.action import Node
#import networkx as nx

class BooleanModel():
    def __init__(self, rules):
        self.rules = rules
        self.nodes = list(rules.keys())
        self.rule_string = None


    def __copy__(self):
        rules = dict()
        for dst,(act,inh) in self.rules.items():
            rules[dst] = ([],[])
            for src in act:
                rules[dst][0].append(src)
            for src in inh:
                rules[dst][1].append(src)
        return BooleanModel(rules=rules)

    def add(self, action):
        rule_type_idx = 0 if action.type == 'a' else 1
        self.rules[action.dst][rule_type_idx].append(tuple([Node(src.src, src.neg) for src in action.srcs]))

    def print_clause(self, expression):
        rule = []
        for clause in expression:
            c = []
            for src in clause:
                if src.neg:
                    item = f"not {src.src}_{src.idx}"
                else:
                    item = f"{src.src}_{src.idx}"
                c.append(item)
            rule.append(' and '.join(c))
        return ' or '.join(rule)

    def print_rules(self):
        for dst, (activators, inhibitors) in self.rules.items():
            inhibitor_rule = self.print_clause(inhibitors)
            activator_rule = self.print_clause(activators)

            if activator_rule and inhibitor_rule:
                rule = f'({activator_rule}) and not ({inhibitor_rule})'
            elif activator_rule:
                rule = f'({activator_rule})'
            elif inhibitor_rule:
                rule = f'not ({inhibitor_rule})'
            else:
                rule = False
            print(f'{dst} = {rule}')            

    def update_sync(self):
        new_state = dict()
        for node in self.nodes:
            new_state[node] = self.update(node)
        self.state = new_state


    def simulate(self, start_states, return_states=False):
        attractors = defaultdict(lambda:0)
        for start_state in start_states:
            states = dict()
            step = 0
            self.state = start_state
            key = tuple(self.state.items())
            while key not in states:
                #print(step)
                #for k,v in key:
                #    print(k,v)
                #print('-----')
                states[key] = step
                self.update_sync()
                step += 1
                key = tuple(self.state.items())

            # A one step cycle is the same thing as a stable attractor
            # i.e. it never evolves past this one state
            cycle_start = states[key]
            cycle = list(states.keys())[cycle_start:]
            
            # put the cycle in a canonical ordering 
            # compute the binary representation of the state, order by 
            # the integer value of the the binary representation
            smallest = float('inf')
            for i,state in enumerate(cycle):
                value = to_int(state)
                if value < smallest:
                    smallest = value
                    start_idx = i
            cycle = rotate_list(cycle, start_idx)
            attractors[tuple(cycle)] += 1

        if not return_states:
            return dict(attractors)
        else:
            return (dict(attractors), list(states.keys()))
        

    def simulate_random(self, p, num_starts):
        start_states = []
        start_set = set()
        for i in range(num_starts):
            values = [random.random() > p for _ in range(len(self.nodes))]
            start_key = tuple(values)
            while start_key in start_set:
                values = [random.random() > p for _ in range(len(self.nodes))]
                start_key = tuple(values)
            start_set.add(start_key)
            start_state = dict(zip(self.rules.keys(), values))
            start_states.append(start_state)
        attractors = self.simulate(start_states) 
        return start_states, attractors

    def update(self, node):
        activators, inhibitors = self.rules[node]

        state = []
        or_clause = []
        # or clause
        for inhibitor in inhibitors:
            # And clause, taking into account negation with neg
            and_clause = [self.state[src] if not src.neg else not self.state[src] for src in inhibitor]
            or_clause.append(all(and_clause))
        if inhibitors:
            state.append(not any(or_clause))

        or_clause = []
        for activator in activators:
            and_clause = [self.state[src] if not src.neg else not self.state[src] for src in activator]
            or_clause.append(all(and_clause))
        if activators:
            state.append(any(or_clause))

        return len(state)>0 and all(state)
    
    # TODO make state probs a sequence
    # Currently they're aggregated. Disaggregate so that we can see trajectories 
    # TODO make states not a boolean string. Too hard to interpret
    # TODO calculate percentage of new states added? Like, what's the (rolling) probability that the next state visited is not a state that we've visited before? This could give us a quantitative measure of whether we've "saturated" the state transition graph, and we can stop simulating?
    def simulate_async(self, start_states, num_starts, num_steps, normalize=True):
        num_nodes = len(self.nodes)
        state_probs = {} 
        total_steps = num_starts * num_steps

        start_states, start_probs = zip(*start_states)
        for start in random.choices(start_states, weights=start_probs, k=num_starts):
            self.state = copy(start)
            state_key = tuple(self.state.items())
            if state_key not in state_probs:
                state_probs[state_key] = 0
            state_probs[state_key] += 1
            # minus one to account for the first step (initial point)
            for step in range(num_steps-1):
                node = random.choice(self.nodes)
                self.state[node] = self.update(node)
                state_key = tuple(self.state.items())
                if state_key not in state_probs:
                    state_probs[state_key] = 0
                state_probs[state_key] += 1

        if normalize:
            for state in state_probs:
                state_probs[state] = state_probs[state]/total_steps

        return state_probs

        
    def simulate_all(self):
        # TODO this creates an explicit list of start states, which will take forever for large states
        start_states = list(product([True,False], repeat=len(self.edges)))
        start_states = [dict(zip(self.edges.keys(),start_state)) for start_state in start_states]
        #TODO convert to 
        attractors = self.simulate(start_states)
        return attractors
