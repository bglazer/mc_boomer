#####################
# Initial States
#####################
wild_type_initial = [dict([
    (('wg', 0) , False), (('wg', 1) , True ), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , True ), (('en', 3) , False), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , False), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ), 
    (('PTC', 0), False), (('PTC', 1), False), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ), 
    (('CI', 0) , False), (('CI', 1) , False), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
])]

en_knockout_initial = [dict([
    (('wg', 0) , False), (('wg', 1) , True ), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , False ), (('en', 3) , False), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , False), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ), 
    (('PTC', 0), False), (('PTC', 1), False), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ), 
    (('CI', 0) , False), (('CI', 1) , False), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
])]

wg_knockout_initial = [dict([
    (('wg', 0) , False), (('wg', 1) , False), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , True ), (('en', 3) , False), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , False), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ), 
    (('PTC', 0), False), (('PTC', 1), False), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ), 
    (('CI', 0) , False), (('CI', 1) , False), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
])]

wg_overexpression = [dict([
    (('wg', 0) , True ), (('wg', 1) , True ), (('wg', 2) , True ), (('wg', 3) , True ), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , True ), (('en', 3) , False), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , False), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ), 
    (('PTC', 0), False), (('PTC', 1), False), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ), 
    (('CI', 0) , False), (('CI', 1) , False), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
])]

en_overexpression = [dict([
    (('wg', 0) , False), (('wg', 1) , True ), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , True ), (('en', 1) , True ), (('en', 2) , True ), (('en', 3) , True ), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , False), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ), 
    (('PTC', 0), False), (('PTC', 1), False), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ), 
    (('CI', 0) , False), (('CI', 1) , False), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
])]

hh_overexpression = [dict([
    (('wg', 0) , False), (('wg', 1) , True ), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , True ), (('en', 3) , False), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , True ), (('hh', 1) , True ), (('hh', 2) , True ), (('hh', 3) , True ), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ), 
    (('PTC', 0), False), (('PTC', 1), False), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ), 
    (('CI', 0) , False), (('CI', 1) , False), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
])]

#####################
# Attractors
#####################

wild_type_true_attractors = {((
    (('wg', 0) , False), (('wg', 1) , True ), (('wg', 2) , False), (('wg', 3) , False),
    (('WG', 0) , False), (('WG', 1) , True ), (('WG', 2) , False), (('WG', 3) , False),
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , True ), (('en', 3) , False),
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , True ), (('EN', 3) , False),
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , False),
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , True ), (('HH', 3) , False),
    (('ptc', 0), False), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), True ),
    (('PTC', 0), True ), (('PTC', 1), True ), (('PTC', 2), False), (('PTC', 3), True ),
    (('PH', 0) , False), (('PH', 1) , True ), (('PH', 2) , False), (('PH', 3) , True ),
    (('SMO', 0), False), (('SMO', 1), True ), (('SMO', 2), True ), (('SMO', 3), True ),
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , True ),
    (('CI', 0) , True ), (('CI', 1) , True ), (('CI', 2) , False), (('CI', 3) , True ),
    (('CIA', 0), False), (('CIA', 1), True ), (('CIA', 2), False), (('CIA', 3), True ),
    (('CIR', 0), True ), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False),
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
),):1}

initial_perturb_true_attractors = {((
    (('wg', 0) , True ), (('wg', 1) , True ), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , True ), (('WG', 1) , True ), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , True ), (('en', 3) , True ), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , True ), (('EN', 3) , True ), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , True ), (('hh', 3) , True ), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , True ), (('HH', 3) , True ), 
    (('ptc', 0), True ), (('ptc', 1), True ), (('ptc', 2), False), (('ptc', 3), False), 
    (('PTC', 0), True ), (('PTC', 1), True ), (('PTC', 2), False), (('PTC', 3), False), 
    (('PH', 0) , True ), (('PH', 1) , True ), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), True ), (('SMO', 1), True ), (('SMO', 2), True ), (('SMO', 3), True ), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , False), (('ci', 3) , False), 
    (('CI', 0) , True ), (('CI', 1) , True ), (('CI', 2) , False), (('CI', 3) , False), 
    (('CIA', 0), True ), (('CIA', 1), True ), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), False), (('CIR', 1), False), (('CIR', 2), False), (('CIR', 3), False), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
),):1}

knockout_true_attractors = {((
    (('wg', 0) , False), (('wg', 1) , False), (('wg', 2) , False), (('wg', 3) , False), 
    (('WG', 0) , False), (('WG', 1) , False), (('WG', 2) , False), (('WG', 3) , False), 
    (('en', 0) , False), (('en', 1) , False), (('en', 2) , False), (('en', 3) , False), 
    (('EN', 0) , False), (('EN', 1) , False), (('EN', 2) , False), (('EN', 3) , False), 
    (('hh', 0) , False), (('hh', 1) , False), (('hh', 2) , False), (('hh', 3) , False), 
    (('HH', 0) , False), (('HH', 1) , False), (('HH', 2) , False), (('HH', 3) , False), 
    (('ptc', 0), False), (('ptc', 1), False), (('ptc', 2), False), (('ptc', 3), False), 
    (('PTC', 0), True ), (('PTC', 1), True ), (('PTC', 2), True ), (('PTC', 3), True ), 
    (('PH', 0) , False), (('PH', 1) , False), (('PH', 2) , False), (('PH', 3) , False), 
    (('SMO', 0), False), (('SMO', 1), False), (('SMO', 2), False), (('SMO', 3), False), 
    (('ci', 0) , True ), (('ci', 1) , True ), (('ci', 2) , True ), (('ci', 3) , True ), 
    (('CI', 0) , True ), (('CI', 1) , True ), (('CI', 2) , True ), (('CI', 3) , True ), 
    (('CIA', 0), False), (('CIA', 1), False), (('CIA', 2), False), (('CIA', 3), False), 
    (('CIR', 0), True ), (('CIR', 1), True ), (('CIR', 2), True ), (('CIR', 3), True ), 
    (('SLP', 0), True ), (('SLP', 1), True ), (('SLP', 2), False), (('SLP', 3), False),
),):1}
