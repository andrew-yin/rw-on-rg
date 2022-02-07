import random

class Walker:

    def __init__(self, strategy, graph, start):
        self.strategy = strategy
        self.graph = graph
        self.start = start
        self.cur = start
        self.path = [start]
        self.neighbors = {node: list(neighbors.keys()) for node, neighbors in self.graph.adj.items()}

    def move(self):
        if self.strategy == "random":
            neighbors = [i[0] for i in self.graph.adj[self.cur].items()]
            if len(neighbors) != 0:
                self.cur = random.choice(neighbors)

    
    def move_dict(self):
        if self.strategy == "random":
            if len(self.neighbors[self.cur]) != 0:
                self.path.append(random.choice(self.neighbors[self.cur]))

    def get_current_node(self):
        return self.cur
