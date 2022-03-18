from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice

class DWRandomGreedyOmniscient(DualWalker):
    """
    Greedy Omniscient walker knows the nodes rw has visited 
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

            not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
            if len(not_claimed) != 0: 
                self.cur2 = choice(tuple(not_claimed))
            else:
                self.cur2 = choice(self.neighbors[self.cur2])
            self.claimed2.add(self.cur2)    

        if flip == 1: 
            not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
            if len(not_claimed) != 0: 
                self.cur2 = choice(tuple(not_claimed))
            else:
                self.cur2 = choice(self.neighbors[self.cur2])
            self.claimed2.add(self.cur2) 

            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)