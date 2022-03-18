from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice

class DWRandomNoBackTrack(DualWalker):
    """
    The agent will not back track
    """
    def __init__(self):
        self.claimed1 = None
        self.claimed2 = None
        self.past2 = None

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
        self.past2 = self.cur2


    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None
        self.past2 = None

    def move(self,flip):

        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

            if self.past2 == self.cur2:
                self.cur2 = choice(self.neighbors[self.cur2])
            else:
                neighbors_noback = set(self.neighbors[self.cur2]) - {self.past2}
                if len(neighbors_noback) != 0:
                    self.past2 = self.cur2
                    self.cur2 = choice(tuple(neighbors_noback))
                else:
                    self.past2, self.cur2 = self.cur2, self.past2
             

        if flip == 1: 
            if self.past2 == self.cur2:
                self.cur2 = choice(self.neighbors[self.cur2])
            else:
                neighbors_noback = set(self.neighbors[self.cur2]) - {self.past2}
                if len(neighbors_noback) != 0:
                    self.past2 = self.cur2
                    self.cur2 = choice(tuple(neighbors_noback))
                else:
                    self.past2, self.cur2 = self.cur2, self.past2


            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)