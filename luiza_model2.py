from tomato.classes import cell
import numpy as np
from numpy import random


# 0 --> Neutral
# 1 --> Believer
# 2 --> BD
# 3 --> FC
# 4 --> Skeptical
# 5 --> SD

class Cell(cell.CellTemplate):
    colors = (
        (244,164,96), #N laranja 0
        (135,206,250), #B azul 1
        (169,169,169), #BD cinza 2
        (144,238,144), #FC verde 3
        (255,182,193), #S rosa 4
        (240,230,140)  #SD amarelo 5
    )
    
    def __init__(self,val,pos,cell_args):
        self.lin, self.col = pos
        self.value = val

        self.prob = cell_args[0][self.lin, self.col]
        self.alpha = cell_args[1]
        
        global rng
        global random_neighbors_num
        
        rng = np.random.default_rng(cell_args[2])
        random_neighbors_num = cell_args[3]
        
    def update(self, state_matrix):
        self.state_matrix = state_matrix

        if self.value == 0:
            if self.believing_ratio >= .5:
                self.value = 1
            elif self.believing_ratio < .5 and self.believing_ratio >= .1:
                if random.rand() > .7:
                    self.value = 3
                else:
                    self.value = 0
            else:
                self.value = 4
        
        elif self.value == 1:
            if self.believing_ratio >= .5:
                if random.rand() > .7:
                    self.value = 2
                else:
                    self.value = 1
            elif self.believing_ratio < .5 and self.believing_ratio >= .3:
                self.value = 1
            else:
                self.value = 3
                
        elif self.value == 3:
            if self.believing_ratio >= .8:
                self.value = 1
            elif self.believing_ratio >= 0.6 and self.believing_ratio < 0.8:
                self.value = 0
            else:
                if random.rand() > .5:
                    self.value = 4
                else:
                    self.value = 3
                
        elif self.value == 4:
            if self.believing_ratio <= .3:
                if random.rand() > .8:
                    self.value = 5
                else:
                    self.value = 4
            elif self.believing_ratio > .6:
                self.value = 3
            else:
                self.value = 4

    @property
    def neighbors(self):
        return self.moore_neighborhood
    
    @property
    def rand_neighbors(self):
        # {{{
        global rng
        global random_neighbors_num

        return rng.choice(self.state_matrix.flatten(), random_neighbors_num)
    # }}}

    @property
    def believing_ratio(self):
        B = self.neighbors.count(1) + list(self.rand_neighbors).count(1)
        BD = self.neighbors.count(2) + list(self.rand_neighbors).count(2)
        SD = self.neighbors.count(5) + list(self.rand_neighbors).count(5)
        S = self.neighbors.count(4) + list(self.rand_neighbors).count(4)
        # B = self.neighbors.count(1)
        # BD = self.neighbors.count(2)
        # SD = self.neighbors.count(5)
        # S = self.neighbors.count(4)
        P = self.prob
        alfa = self.alpha
        gama = 0.2
        beta = 0.4
        delta = 0.3
        psi = 0.1
        viz = (alfa/(8))*(2*BD + B - 2*SD)
        prob = (1-alfa)*P
        if viz >= 0:
            return viz+prob
        else:
            return prob
    
    @staticmethod
    def display(value):
        return Cell.colors[value]
        
    @staticmethod
    def from_display(value):
        return Cell.colors.index(tuple(value))