from mc_boomer.linear_model import LinearModel

class SegmentPolarityModel(LinearModel):
    def update_sync(self):
        new_state = dict()
        exec(self.update)
        self.state = new_state
        # TODO add explicit control of constitutively activated patterns
        # SLP is constituitively expressed in the following pattern, repeating every 4 cells:
        # True True False False 
        # The code below recreates this pattern for any number of cells
        for i in range(self.num_cells):
            self.state[('SLP',i)] = True if (i+1) % 4 in (1,2) else False
