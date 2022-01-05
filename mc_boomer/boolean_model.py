from collections import defaultdict
from itertools import product
from copy import copy
import random
from mc_boomer.util import bool_state, to_int, rotate_list
#import networkx as nx

class BooleanModel():
    def __init__(self, rules):
        self.rules = rules
        self.nodes = list(rules.keys())
        self.changed = False


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
        self.rules[action.dst][rule_type_idx].append(action.srcs)
        self.changed = True

    def print_expression(self, expression):
        rule = []
        for clause in expression:
            c = []
            for src, cell_idx in clause:
                if src[0] == '~':
                    src = src[1:]
                    item = f'not {src}_{cell_idx}'
                else:
                    item = f'{src}_{cell_idx}'
                c.append(item)
            rule.append(' and '.join(c))
        return ' or '.join(rule)

    def compile_expression(self, expression):
        rule = []
        for clause in expression:
            c = []
            for src in clause:
                if src[0] == '~':
                    src = src[1:]
                    item = f"not self.state['{src}']"
                else:
                    item = f"self.state['{src}']"
                c.append(item)
            rule.append(' and '.join(c))
        return ' or '.join(rule)
        
    def compile_rules(self, verbose=False):
        self.update = {}
        rules = []
        # Create a string with all the code for all the update rules 
        for dst, (activators, inhibitors) in self.rules.items():
            inhibitor_rule = self.compile_expression(inhibitors)
            activator_rule = self.compile_expression(activators)

            if activator_rule and inhibitor_rule:
                rule = f'({activator_rule}) and not ({inhibitor_rule})'
            elif activator_rule:
                rule = f'({activator_rule})'
            elif inhibitor_rule:
                rule = f'not ({inhibitor_rule})'
            else:
                rule = False
            rule_string = f'new_state[{dst}] = {rule}'

            # Compile the string into Python bytecode that we can exec later
            if verbose:
                print(rule_string)
            self.update[dst] = compile(rule_string, filename=str(dst),  mode='exec', optimize=2)


    def update_sync(self):
        new_state = dict()
        for dst in self.update:
            exec(self.update[dst])
        self.state = new_state


    def simulate(self, start_states, return_states=False, fresh_compile=False):
        self.compile_rules()
        attractors = defaultdict(lambda:0)
        for start_state in start_states:
            states = dict()
            step = 0
            self.state = start_state
            key = tuple(self.state.items())
            while key not in states:
                states[key] = step
                self.update_sync()
                step += 1
                key = tuple(self.state.items())

            # A one step cycle is the same thing as a stable attractor
            # i.e. it never evolves past this one state
            cycle_start = states[key]
            # for cyclic attractors, grab every state until the start of the cycle
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
        self.compile_rules(verbose=True)
        attractors = self.simulate(start_states) 
        return start_states, attractors

    def update_async(self, node):
        new_state = self.state
        exec(self.update[node])
        self.state = new_state

    
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
                self.update_async(node)
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
