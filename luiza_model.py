from tomato.classes import cell
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

        self.prob = cell_args[self.lin, self.col]
        #self.alpha = cell_args[1]
        
    def update(self, state_matrix):
        self.state_matrix = state_matrix

        
        if self.value == 0:
            if self.believing_ratio >= .5:
                self.value = 1
            elif self.believing_ratio < .5 and self.believing_ratio >= .1:
                if random.rand() > .9:
                    self.value = 3
                else:
                    self.value = 0
            else:
                self.value = 4
        
        elif self.value == 1:
            if self.believing_ratio >= .5:
                self.value = 2
            elif self.believing_ratio < .5 and self.believing_ratio >= .1:
                self.value = 1
            else:
                self.value = 3
                
        elif self.value == 3:
            if self.believing_ratio >= .6:
                self.value = 1
            else:
                if random.rand() > .5:
                    self.value = 4
                else:
                    self.value = 3
                
        elif self.value == 4:
            if self.believing_ratio <= .2:
                self.value = 5
            elif self.believing_ratio > .6:
                self.value = 3
            else:
                self.value = 4

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def believing_ratio(self):
        B = self.neighbors.count(1)
        BD = self.neighbors.count(2)
        SD = self.neighbors.count(5)
        S = self.neighbors.count(4)
        P = self.prob
        alfa = 1.0
        gama = 0.2
        beta = 0.4
        delta = 0.3
        psi = 0.1
        result = 0.5*(P+(alfa/(8*delta))*(gama*B+delta*BD-beta*SD-psi*S))
        if result >= 0:
            return result
        else:
            return 0
    
    @staticmethod
    def display(value):
        return Cell.colors[value]
        
    @staticmethod
    def from_display(value):
        return Cell.colors.index(tuple(value))