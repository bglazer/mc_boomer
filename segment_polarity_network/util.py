nodes = ['wg', 'WG', 'en', 'EN', 'hh', 'HH', 'ptc', 'PTC', 'PH', 'SMO', 'ci', 'CI', 'CIA', 'CIR', 'SLP']

def print_state(state, num_cells=4):
    for node in nodes:
        bs=[]
        for cell in range(num_cells):
            value = state[(node,cell)]
            ov = '1' if value else '0'
            bs.append(ov)
        print(f'{node:.<4}{"".join(bs)}')


def print_attractors(attractors, truth=None, squashed=False, num_cells=4, latex=False):
    if latex:
        correct = '$\colorbox{{Gray}}{{{}}}}'
        incorrect = '$\colorbox{{CornflowerBlue}}{{{}}}'
        line= '\\texttt{{{node:.<4}{cells}}}\n'
    else:
        incorrect = 'x{}'
        correct = ' {}'
        line = '{node: <4}{cells}'
    #stable, cyclic = attractors

    #true_stable, true_cyclic = truth
    if squashed:
        attractors = convert_cyclic(attractors)
        for attractor, count in attractors.items():
            attractor = dict(attractor)
            for node in nodes:
                bs=[]
                for cell in range(num_cells):
                    value = attractor[(node,cell)]
                    bs.append(f'{value:.2f}')
                print(line.format(node=node, cells=" ".join(bs)))

    else:
        #truth = dict(list(truth.keys())[0])
        if truth:
            truth = dict(list(truth.keys())[0][0])
        else:
            truth=None

        for cycle, count in attractors.items():
            step_idx = 0
            for node in nodes:
                bs=[]
                for step in cycle:
                    step = dict(step)
                    for cell in range(num_cells):
                        value = step[(node,cell)]
                        if truth:
                            true_value = truth[(node,cell)]
                        else:
                            true_value = value
                        ov = '1' if value else '0'
                        if value == true_value:
                            bs.append(correct.format(ov))
                        else:
                            bs.append(incorrect.format(ov))
                    bs.append(' ')
                #print('\\texttt{' + f'{node:.<4}{"".join(bs)}' + '}')
                print(line.format(node=node, cells=" ".join(bs)))

def print_async_attractors(attractors, num_cells=4):
    line = '{node: <4}{cells}'
    for attractor, prob in attractors:
        print(prob)
        attractor = dict(attractor)
        for node in nodes:
            bs=[]
            for cell in range(num_cells):
                value = attractor[(node,cell)]
                bs.append(f'{value:1d}')
            print(line.format(node=node, cells=" ".join(bs)))
        print('-')
