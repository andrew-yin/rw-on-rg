import random

class Walker:

    def __init__(self, strategy, graph=None):
        self.strategy = strategy
        self.graph = graph
        self.cur = None

    def load_graph(self, graph):
        self.graph = graph
        if self.strategy == "random":
            self.cur = random.choice(list(self.graph))

    def reset(self):
        self.graph = None

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
