from random import choice

from walkers.walker import Walker


class GreedyWalker(Walker):
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
        if len(self.neighbors[self.cur]) != 0:
            if len(set(self.neighbors[self.cur]) - self.visited) == 0:
                self.cur = choice(self.neighbors[self.cur])
                return False
            else:
                self.cur = choice(list(set(self.neighbors[self.cur]) - self.visited))
                self.visited.add(self.cur)
                return True