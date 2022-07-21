from tomato.classes import cell

# 0 --> Neutral
# 1 --> Believer
# -1 --> Skeptical

class Cell(cell.CellTemplate):
    
    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Dead cell
        
        if self.value == 0:
            if self.live_neighbors_b >= 5:
                self.value = 1
            elif self.live_neighbors_s >= 6:
                self.value = -1
            else:
                self.value = 0
                
        # Live cell
        
        elif self.value == 1:
            if self.live_neighbors_s in (5, 6):
                self.value = 0
            elif self.live_neighbors_s >= 7:
                self.value = -1
            else:
                self.value = 1
                
        else:
            if self.live_neighbors_b in (5,6):
                self.value = 0
            elif self.live_neighbors_b >= 7:
                self.value = 1
            else:
                self.value = -1

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def live_neighbors_b(self):
        return self.neighbors.count(1)
    
    @property
    def live_neighbors_s(self):
        return self.neighbors.count(-1)
    
    @staticmethod
    def display(value):
        if value == 0:
            return (169,169,169)
        elif value == 1: 
            return (139,0,0)
        else:
            return (70,130,180)
        
    @staticmethod
    def from_display(value):
        if (value == (169,169,169)).all():
            return 0
        elif (value == (139,0,0)).all():
            return 1
        else:
            return -1