from itertools import permutations, product
from segment_polarity_model import SegmentPolarityModel
from mc_boomer.action import Action, Source

def emptyModel():
    num_cells = 4
    # Canonical species for segment polarity network according to doi:10.1016/S0022-5193(03)00035-3
    species = ['EN', 'en', 'SLP', 'wg', 'ptc', 'CIR', 'CIA', 'CI', 'ci', 'hh', 'HH', 'PH', 'WG', 'SMO', 'PTC']
    # Create a node copy for every cell 
    rules = {}
    for cell_idx in range(num_cells):
        for node in species:
            node_cell = (node,cell_idx)
            rules[node_cell] = ([],[])

    # initialize empty model
    spm = SegmentPolarityModel(num_cells=num_cells, rules=rules)
    return spm
    
def allActions():
    genes = ['en','wg','ci','ptc','hh']
    proteins = ['EN', 'SLP', 'CIR', 'CIA', 'CI']
    membranes = ['HH', 'PH', 'SMO', 'PTC', 'WG']

    internal_rules = list(permutations(proteins + membranes, r=2))
    external_rules = list(permutations(membranes, r=2))
    transcription_factor_rules = list(product(proteins, genes))

    num_rules = len(internal_rules)+len(external_rules)+len(transcription_factor_rules)

    actions = set()
    for src,dst in internal_rules:
        actions.add(Action(srcs=(Source(span='i', src=src),), type='a', dst=dst))
        actions.add(Action(srcs=(Source(span='i', src=src),), type='i', dst=dst))

    for src,dst in transcription_factor_rules:
        actions.add(Action(srcs=(Source(span='i', src=src),), type='a', dst=dst))
        actions.add(Action(srcs=(Source(span='i', src=src),), type='i', dst=dst))

    for src,dst in external_rules:
        actions.add(Action(srcs=(Source(span='e', src=src),), type='a', dst=dst))
        actions.add(Action(srcs=(Source(span='e', src=src),), type='i', dst=dst))

    # Create compound actions
    # We choose the compounds assuming prior knowledge that only the species
    # form active compounds with each other
    compounds = [(Source('CIA','i'), Source('SLP','i')), 
                 (Source('CI','i'),  Source('SMO','i')),
                 (Source('CI','i'),  Source('HH','e')),
                 ]
                 # Already set as an action below
                 #(Source('PTC','i'), Source('HH','e')),
    for compound,dst in list(product(compounds, genes)) + list(product(compounds, proteins)):
        actions.add(Action(srcs=compound, dst=dst, type='i'))
        actions.add(Action(srcs=compound, dst=dst, type='a'))

    wg_actions = [
                 Action(srcs=(Source('CIA','i'), Source('wg','i')), dst='wg', type='a'),
                 Action(srcs=(Source('CIA','i'), Source('wg','i')), dst='wg', type='i'),
                 Action(srcs=(Source('SLP','i'), Source('wg','i')), dst='wg', type='a'),
                 Action(srcs=(Source('SLP','i'), Source('wg','i')), dst='wg', type='i'),
                 ]
    for action in wg_actions:
        actions.add(action)


    return actions

def addPrior(actions):
    prior = 1/(len(actions))
    ax = {action: prior for action in actions}
    ax['stop'] = 0.0
    return ax

def initialState():

    spm = emptyModel()

    actions = allActions()

    # Initialize the genes to be activating the proteins.
    # We can assume this is true apriori
    gene_protein_rules = [Action(srcs=(Source(span='i',src='en'),), type='a', dst='EN'),
                          Action(srcs=(Source(span='i',src='wg'),), type='a', dst='WG'),
                          Action(srcs=(Source(span='i',src='ci'),), type='a', dst='CI'),
                          Action(srcs=(Source(span='i',src='ptc'),), type='a',dst='PTC'),
                          Action(srcs=(Source(span='i',src='hh'),), type='a', dst= 'HH')]

    # Initialize CI to activate CIA and CIR, because these are truncated CI protein
    ci_rules = [Action(srcs=(Source(span='i',src='CI'),), type='a', dst='CIA'),
                Action(srcs=(Source(span='i',src='CI'),), type='a', dst='CIR')]

    # Initialize PTC and HH (external) to activate PH, because its a complex
    # Maybe we could remove PH entirely because it's just a compound??
    ph_rule = [Action(srcs=(Source('PTC','i'), Source('HH','e')), dst ='PH', type='a')]

    # The rules below aren't explicitly prior knowledge
    # They just represent some weird interactions that don't fit the "normal"
    # modeling paradigm that we're assuming

    # These two rules include negations, which we assume some prior knowledge. 
    # So we just add them directly. This could be relaxed, but then we'd have to add a bunch of 
    # additional actions that include one or both terms negated. That would explode the search 
    # space. 
    ptc_rule = [Action(srcs=(Source('PTC','i'), Source('~HH','e')), dst='PTC', type='a')]
    smo_rule = [Action(srcs=(Source('~PTC','i'),), dst='SMO', type='a')]

    # These are weird interactions in Reka's model where a membrane protein can directly
    # activate/inhibit internal proteins in another cell
    # Should these be prior knowledge?
    external_internal_rules = [
        Action(srcs=(Source(src='HH', span='e'),), dst='CIR', type='i'),
        Action(srcs=(Source(src='WG', span='e'),), dst='en', type='a')
    ]

    # Aggregate all the rules that we manually specify
    custom_rules = ci_rules + gene_protein_rules + ph_rule + ptc_rule + smo_rule + external_internal_rules
    for action in custom_rules:
        spm.add(action)
        if action in actions:
            actions.remove(action)

    # Remove CIA inhibition actions
    # Remove CIR activation actions
    #  CIA is defined as an activator, and CIR as inhibitor. 
    #  This is kind of questionable though
    #  This is the kind of prior knowledge constraint that 
    #  could be relaxed justifiably
    # Remove SLP target actions, it's constituitively expressed in a specific pattern,
    #  so it doesn't make sense to have other nodes try to influence it
    for action in list(actions):
        if len(action.srcs) == 1:
            (src, span), = action.srcs
            if ((src == 'CIA' and action.type == 'i') or \
                (src == 'CIR' and action.type == 'a')):
                actions.remove(action)
        if action.dst == 'SLP' and action in actions:
            actions.remove(action)

    return spm, addPrior(list(actions))
