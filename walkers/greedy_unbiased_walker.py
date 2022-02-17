from random import choice

from walkers.walker import Walker


class GreedyUnbiasedWalker(Walker):
    """
    A greedy unbiased walker. At each step, pick a random node not visited and move there. If all neighbors have been visited, random pick one. 
    """

    def __init__(self):
        self.visited = None

    def reset(self):
        super().reset()
        self.visited = None

    def load_graph(self, graph):
        super().load_graph(graph)
        self.cur = choice(list(self.graph))
        self.visited = {self.cur}

    def move(self):
        not_visited = set(self.neighbors[self.cur]) - self.visited
        if len(not_visited) != 0:
            self.cur = choice(tuple(not_visited))
            self.visited.add(self.cur)
        else:
            self.cur = choice(self.neighbors[self.cur])
