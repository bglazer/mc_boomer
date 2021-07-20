from __future__ import division

import time
import math
import random

import heapq

#import networkx as nx
import pickle
import json
import gzip
from mc_boomer.util import gteq


def randomPolicy(state):
    while not state.isTerminal():
        try:
            action,prior = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state

def biasedRandomPolicy(state):
    action_sequence = []
    while not state.isTerminal():
        try:
            actions,priors = zip(*state.getPossibleActions())
            action = random.choices(actions, weights=priors)[0]
            action_sequence.append(action)
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state, action_sequence

def explorationDecay(percentComplete):
    return 1 - percentComplete**3

def constantExploration(percentComplete):
    return 1

class treeNode():
    def __init__(self, state, parent, prior):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.bestReward = 0
        self.children = {}
        self.prior = prior

class boundedheap():
    def __init__(self, max_size):
        self.l = []
        self.max_size = max_size 
    
    def push(self, x):
        key, value = x
        if len(self.l) >= self.max_size:
            smallestkey = self.l[0][0]
            if key > smallestkey:
                heapq.heappop(self.l)
                heapq.heappush(self.l, x)
        # automatically push if the heap is not full yet
        else:
            heapq.heappush(self.l, x)
        

class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=0.1,
                 explorationPolicy=constantExploration, rolloutPolicy=biasedRandomPolicy, 
                 rave_equiv_param=None, cache=False, nested=False, threshold=0.0,
                 model_file=None, run_file=None, stats_file=None, tree_file=None, num_saved_models=500):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.iterationLimit = iterationLimit
            self.limitType = 'iterations'

        self.explorationConstant = explorationConstant
        self.explorationPolicy = explorationPolicy
        self.rollout = rolloutPolicy
        # TODO add argument for number of models to keep
        #self.best_states = boundedheap(num_saved_models)
        self.best_reward = 0
        self.sim_count = 0
        self.threshold = threshold
        if stats_file is not None:
            self.stats_file = open(stats_file, 'w')
            self.stats_file.write('step,depth,reward\n')
            self.write_stats = True
        else:
            self.write_stats = False

        if model_file is not None:
            self.model_file = gzip.open(model_file, 'wb')
        else:
            raise Exception("Must provide model_file parameter")
        self.tree_file = tree_file
        self.run_file = run_file
        self.cache = cache
        #TODO make argument
        self.nested = nested
        if self.cache:
            self.state_cache = dict()

        if rave_equiv_param is None:
            self.rave = False
        else:
            self.rave = True
            self.rave_stats = dict()
            self.rave_equiv_param = rave_equiv_param

    # Save the tree in a compressed format
    #def saveTree(self, tree_file):
    #    tree = nx.DiGraph()
    #    i = 0 
    #    tree.add_node(i)
    #    stack = []
    #    stack.append((i,self.root))
    #    while len(stack) > 0:
    #        index, node = stack.pop()
    #        children = node.children.values()
    #        for child in children:
    #            i += 1
    #            stack.append((i,child))
    #            tree.add_edge(index, i)

    #    pickle.dump(tree, open(tree_file, 'wb'))
    
    def countTree(self):
        i = 0 
        stack = []
        stack.append((i,self.root))
        while len(stack) > 0:
            index, node = stack.pop()
            children = node.children.values()
            for child in children:
                i += 1
                stack.append((i,child))
        return i

    def search(self, initialState=None, rootNode=None):
        if initialState is not None and rootNode is None:
            self.root = treeNode(initialState, None, 0.0)
        elif initialState is None and rootNode is not None:
            self.root = rootNode
        else:
            raise Exception('Exactly one of initialState or rootNode should be supplied')

        self.step = 0
        if self.limitType == 'time':
            t = time.time()
            timeLimit = t + self.timeLimit / 1000
            percentComplete = t/(t + self.timeLimit/1000)
            while time.time() < timeLimit:
                self.executeRound(percentComplete)
                self.step += 1
        else:
            for i in range(self.iterationLimit):
                percentComplete = i / self.iterationLimit
                self.step = i
                self.executeRound(percentComplete)

        bestChild, action = self.getBestChild(self.root, explorationValue=0)

        # TODO, should this only apply when explorationValue = 0?
        # i.e. when we're selecting a child for a move, not for exploration

        if self.nested:
            #print(self.best_sequence, file=self.run_file, flush=True)
            best_sequence_action = self.best_sequence.pop(0)
            if gteq(self.best_reward, bestChild.bestReward):
                print('nested', file=self.run_file)
                if best_sequence_action in self.root.children:
                    bestChild = self.root.children[best_sequence_action]
                else:
                    nextState = self.root.state.takeAction(best_sequence_action)
                    bestChild = treeNode(nextState, None, 0)
                action = best_sequence_action

        # only save the tree if a filename is provided
        if self.tree_file is not None:
            self.saveTree(self.tree_file)

        return action, bestChild


    def executeRound(self, percentComplete):
        exploration = self.explorationConstant * self.explorationPolicy(percentComplete)
        depth, node, actions = self.selectNode(self.root, exploration)
        result, rollout_actions = self.rollout(node.state)
        sequence = actions + rollout_actions

        if self.cache:
            result.model.compile_rules()
            cache_key = hash(result.model.rule_string)
            if cache_key not in self.state_cache:
                reward = result.getReward()
                pickle.dump((reward, result.model.rules), self.model_file)
                self.state_cache[cache_key] = reward
            else:
                reward = self.state_cache[cache_key]
        else:
            reward = result.getReward()
            #rules_single_line = result.model.rule_string.replace('\n','\t')
            #self.model_file.write(f'{reward}, "{rules_single_line}"\n')
            if reward >= self.threshold:
                pickle.dump((reward, result.model.rules), self.model_file)
            
        # checking approximate >= for floating point numbers
        if gteq(reward, self.best_reward):
            if reward > self.best_reward:
                print('best reward', reward, file=self.run_file, flush=True)

            self.best_reward = reward
            if self.nested:
                self.best_sequence = sequence

        if self.rave:
            for action in rollout_actions:
                if action in self.rave_stats:
                    rave_count, rave_reward = self.rave_stats[action]
                    rave_count += 1
                    if reward > rave_reward:
                        rave_reward = reward
                    self.rave_stats[action] = (rave_count, rave_reward)
                else:
                    # TODO init'ing rave count = 0 causes division by zero
                    self.rave_stats[action] = (1,0)

        if self.write_stats:
            self.stats_file.write(f'{self.step},{depth},{reward}\n')

        self.sim_count += 1
            
        self.backpropagate(node, reward)

    def selectNode(self, node, exploration):
        depth = 0
        actions = []
        # while not the 'stop' action
        while not node.isTerminal:
            # continue search with child if fully expanded 
            if node.isFullyExpanded:
                node, action = self.getBestChild(node, exploration)
                actions.append(action)
                depth += 1
            # otherwise add a single action child to the node
            # stop the search
            else:
                child, action = self.expand(node)
                actions.append(action)
                return depth, child, actions

        return depth, node, actions

    def expand(self, node):
        actions = node.state.getPossibleActions()
        random.shuffle(actions)
        # following pre-determined list of actions
        for action,prior in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action), node, prior)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return (newNode, action)

        raise Exception("Should never reach here")

    def backpropagate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            #node.totalReward += reward
            if reward > node.bestReward:
                node.bestReward = reward
            node = node.parent

    def getBestChild(self, node, explorationValue, verbose=False):
        bestValue = float("-inf")
        bestNodes = []
        for action, child in node.children.items():
            explore_term = explorationValue * math.sqrt(2 * math.log(node.numVisits) / child.numVisits)
            if self.rave:
                k = self.rave_equiv_param
                if action in self.rave_stats:
                    rave_count, rave_reward = self.rave_stats[action]
                    beta = math.sqrt(k/(3*rave_count+k))
                    nodeValue = (1-beta)*child.bestReward + (beta*rave_reward) + explore_term
                else:
                    rave_reward = child.bestReward
                    nodeValue = child.bestReward + explore_term
            else:
                nodeValue = child.bestReward + explore_term

            if verbose:
                print(action, nodeValue)

            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [(child, action)]
            elif nodeValue == bestValue:
                bestNodes.append((child, action))
        
        choice = random.choice(bestNodes)
            
        return choice

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action
