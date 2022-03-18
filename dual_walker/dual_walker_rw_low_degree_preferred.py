from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice
from numpy import array
from scipy.stats import norm, zscore

class DWRandomLowDegreePreferred(DualWalker):
    """
    The agent will prefer nodes with lower degree (transformation function is the survival function of normal)
    """
    def __init__(self):
        self.claimed1 = None
        self.claimed2 = None
        self.neighbor_prob = {}

    def load_graph(self, graph):
        super().load_graph(graph)

        #choose starting point
        self.cur1 = choice(list(self.graph))
        while len(self.neighbors[self.cur1]) == 0:
            self.cur1 = choice(list(self.graph))
        self.claimed1 = {self.cur1}

        self.cur2 = choice(list(self.graph))
        while len(self.neighbors[self.cur2]) == 0:
            self.cur2 = choice(list(self.graph))
        self.claimed2 = {self.cur2}

        # construct the probability dictionary
        degree_dict = { node:degree for node,degree in graph.degree}
        for i in range(len(graph)):
            neighbor_degrees = array([ degree_dict[neighbor] for neighbor in self.neighbors[i] ])
            if len(set(neighbor_degrees)) > 1:
                neighbor_zscore = zscore(neighbor_degrees)
                neighbor_statistics = 1 - norm(loc = 0, scale = 1).cdf(neighbor_zscore)
                sum_neighbor_stat = sum(neighbor_statistics)
                self.neighbor_prob[i] = neighbor_statistics / sum_neighbor_stat

            elif len(self.neighbors[i]) == 0:
                continue

            else:
                self.neighbor_prob[i] = [1/len(self.neighbors[i])] * len(self.neighbors[i])


    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None
        self.neighbor_prob = {}


    def move(self,flip):

        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

            self.cur2 = choice(self.neighbors[self.cur2], p = self.neighbor_prob[self.cur2])
            self.claimed2.add(self.cur2)    

        if flip == 1: 
            self.cur2 = choice(self.neighbors[self.cur2], p = self.neighbor_prob[self.cur2])
            self.claimed2.add(self.cur2)    

            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)