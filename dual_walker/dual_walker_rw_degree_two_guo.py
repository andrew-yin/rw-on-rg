from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice

class DWRandomDegree2GUO(DualWalker):
    """
    Degree 2 guo is a upgrade of guo.
    The agent first try to see any unclaimed 
    """
    def __init__(self):
        self.claimed1 = None
        self.claimed2 = None

    def load_graph(self, graph):
        super().load_graph(graph)
        self.cur1 = choice(list(self.graph))
        while len(self.neighbors[self.cur1]) == 0:
            self.cur1 = choice(list(self.graph))
        self.claimed1 = {self.cur1}

        self.cur2 = choice(list(self.graph))
        while len(self.neighbors[self.cur2]) == 0:
            self.cur2 = choice(list(self.graph))
        self.claimed2 = {self.cur2}

    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None


    def move(self,flip):

        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

            
            d1_not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
            # first find any unclaimed degree 1 neighbors 
            if len(d1_not_claimed) != 0: 
                self.cur2 = choice(tuple(d1_not_claimed))
            
            # if all degree 1 neighbors are claimed, the agent will see which one is connected to a degree 2 unclaimed neighbor
            else:
                d1_possible = [ d1_neighbor for d1_neighbor in self.neighbors[self.cur2] 
                                    if len( set(self.neighbors[d1_neighbor]) -self.claimed1 - self.claimed2 ) > 0 ]
                
                if len(d1_possible) != 0:
                    self.cur2 = choice(d1_possible)
                else:
                    self.cur2 = choice(self.neighbors[self.cur2])

            self.claimed2.add(self.cur2)    


        if flip == 1: 
            d1_not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
            if len(d1_not_claimed) != 0: 
                self.cur2 = choice(tuple(d1_not_claimed))
            else:
                d1_possible = [ d1_neighbor for d1_neighbor in self.neighbors[self.cur2] 
                                    if len( set(self.neighbors[d1_neighbor]) -self.claimed1 - self.claimed2 ) > 0 ]
                
                if len(d1_possible) != 0:
                    self.cur2 = choice(d1_possible)
                else:
                    self.cur2 = choice(self.neighbors[self.cur2])

            self.claimed2.add(self.cur2)  

            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)