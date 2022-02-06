import random

class Walker:

    def __init__(self, strategy, graph, start):
        self.strategy = strategy
        self.graph = graph
        self.start = start
        self.cur = start

    def move(self):
        if self.strategy == "random":
            neighbors = [i[0] for i in self.graph.adj[self.cur].items()]
            if len(neighbors) != 0:
                self.cur = random.choice(neighbors)

    def get_current_node(self):
        return self.cur