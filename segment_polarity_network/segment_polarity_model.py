from mc_boomer.linear_model import LinearModel

class SegmentPolarityModel(LinearModel):
    def __copy__(self):
        rules = dict()
        for dst,(act,inh) in self.rules.items():
            rules[dst] = ([],[])
            for src in act:
                rules[dst][0].append(src)
            for src in inh:
                rules[dst][1].append(src)
        return SegmentPolarityModel(rules=rules)

    def update_sync(self):
        super().update_sync()
        # TODO add explicit control of constitutively activated patterns
        # SLP is constituitively expressed in the following pattern, repeating every 4 cells:
        # True True False False 
        # The code below recreates this pattern for any number of cells
        for i in range(self.num_cells):
            self.state[('SLP',i)] = True if (i+1) % 4 in (1,2) else False
