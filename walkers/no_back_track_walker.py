from random import choice

from walkers.walker import Walker


class NoBackTrackWalker(Walker):
    """
    A simple walker that just never go back 
    """

    def __init__(self):
        pass


    def load_graph(self, graph):
        super().load_graph(graph)
        self.cur = choice(list(self.graph))
        self.past = self.cur

    def move(self):
        if self.past == self.cur:
            self.cur = choice(self.neighbors[self.cur])
        else:
            neighbors_noback = set(self.neighbors[self.cur]) - {self.past}
            if len(neighbors_noback) != 0:
                self.past = self.cur
                self.cur = choice(tuple(neighbors_noback))
            else:
                self.past, self.cur = self.cur, self.past