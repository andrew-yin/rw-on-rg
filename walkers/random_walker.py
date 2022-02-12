from random import choice

from walkers.walker import Walker


class RandomWalker(Walker):
    """
    A random walker. At each step, pick a random neighbor and move to it.
    """

    def __init__(self):
        pass

    def load_graph(self, graph):
        super().load_graph(graph)
        self.cur = choice(list(self.graph))

    def move(self):
        if len(self.neighbors[self.cur]) != 0:
            self.cur = choice(self.neighbors[self.cur])
