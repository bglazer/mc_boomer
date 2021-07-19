from tree_search import SearchState
import initialize
from mcts import mcts

def search(state, min_edges, max_edges, num_steps=None, search_time=None, 
           stop_prior=.9, explorationConstant=.5, rave_equiv_param=None, cache=False,
           nested=False, explorationPolicy=None, stats_file=None, threshold=0.0, 
           keep_tree=False, run_file=None, model_file=None, tree_file=None):


    if (num_steps is None and search_time is None) or \
       (num_steps is not None and search_time is not None):
        raise Exception('Provide exactly one of num_steps or search_time')


    with open(run_file, 'w') as run_file:
        tree_search = mcts(timeLimit=search_time, 
                           iterationLimit=num_steps, 
                           explorationConstant=explorationConstant, 
                           explorationPolicy=explorationPolicy, 
                           rave_equiv_param=rave_equiv_param,
                           cache=cache,
                           nested = nested,
                           threshold=threshold,
                           stats_file=stats_file, model_file=model_file, run_file=run_file, 
                           tree_file=tree_file)

        print('', file=run_file)
        print('-'*80, file=run_file)
        print('Searching...', file=run_file)
        print('-'*80, file=run_file)
        # By retaining the treeNode from the search, we are also
        # keeping the search statistics associated with it's children
        if keep_tree:
            action, state = tree_search.search(initialState=state)
            isTerminal = state.isTerminal
        else:
            # by using takeAction, we are creating a new "blank"
            # treeNode that doesn't have any search statistics
            action, _ = tree_search.search(initialState=state)
            state = state.takeAction(action)
            isTerminal = state.isTerminal()
        print('move:',action, file=run_file, flush=True)

        while not isTerminal:
            if keep_tree:
                action, state = tree_search.search(rootNode=state)
                state.parent = None
                isTerminal = state.isTerminal
            else:
                action, _ = tree_search.search(initialState=state)
                state = state.takeAction(action)
                isTerminal = state.isTerminal()
            print('move:',action, file=run_file, flush=True)

        print('-'*80, file=run_file)
        print('search complete', file=run_file)
        print('-'*80, file=run_file)
        print('models simulated', file=run_file)
        print(tree_search.sim_count, file=run_file)
        print('-'*80, file=run_file)
        if cache:
            print('unique models found', file=run_file)
            print(len(tree_search.state_cache), file=run_file)
            print('*'*80, file=run_file)
        tree_search.model_file.close()
