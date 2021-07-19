from collections import defaultdict
import random
from util import to_int, rotate_list
from copy import copy
from boolean_model import BooleanModel

class LinearModel(BooleanModel):
    def __init__(self, rules, num_cells=4):
        super.__init__(rules)
        self.num_cells = num_cells


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
            for src, cell_idx in clause:
                if src[0] == '~':
                    src = src[1:]
                    item = f"not self.state[('{src}', {cell_idx})]"
                else:
                    item = f"self.state[('{src}', {cell_idx})]"
                c.append(item)
            rule.append(' and '.join(c))
        return ' or '.join(rule)
        
        
    def add_to_rule(self, action, cell_index, srcs):
        rule_type_idx = 0 if action.type == 'a' else 1
        self.rules[(action.dst, cell_index)][rule_type_idx].append(srcs)
        self.changed = True

    def add(self, action):
        # the model is structured as follows:
        # (node, cell_index): [activating edges], [inhibiting edges]
        # so depending if the action is 'a' or 'i' we choose the right list to update
        # Also, external edges are connected from adjacent cells

        for cell_index in range(0, self.num_cells):
            internals = []
            external_srcs = []
            for src, span in action.srcs:
                # Internal edges
                if span == 'i':
                    internals.append((src, cell_index))

                # External edges, i.e. membrane protein -> membrane protein across cells
                if span == 'e':
                    external_srcs.append(src)

            cell_indexes = []
            # "left" side boundary check
            if cell_index-1 >= 0: 
                cell_indexes.append(cell_index-1)
            # "right" side boundary check
            if cell_index+1 <= spm.num_cells-1:
                cell_indexes.append(cell_index+1)

            if len(external_srcs) > 0:
                external_rules=[]
                for i in cell_indexes:
                    rule = []
                    for ex in external_srcs:
                        rule.append((ex,i))
                    external_rules.append(rule)

                for external in external_rules:
                    self.add_to_rule(action, cell_index, internals+external)
            else:
                self.add_to_rule(action, cell_index, internals)

