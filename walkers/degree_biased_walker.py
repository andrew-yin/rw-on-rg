from numpy.random import choice
from walkers.walker import Walker
import networkx as nx

class DegreeBiasedWalker(Walker):
    def __init__(self):
        pass

    def load_graph(self, graph):
        super().load_graph(graph)
        degree_dict = { node:degree for node,degree in graph.degree}
        neighbors_weighted = {}
        for i in range(len(graph)):
            neighbor_degrees = [ degree_dict[neighbor] for neighbor in self.neighbors[i] ]
            sum_neighbor_dg = sum(neighbor_degrees)
            neighbor_prob = [ nbor_dg/sum_neighbor_dg for nbor_dg in neighbor_degrees ]
            neighbors_weighted[i] = (self.neighbors[i], neighbor_prob)

        self.neighbors_weighted = neighbors_weighted
        self.cur = choice(list(self.graph))

    def move(self):
        self.cur = choice(self.neighbors_weighted[self.cur][0], p = self.neighbors_weighted[self.cur][1])
        