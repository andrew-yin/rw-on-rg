from numpy.random import choice
from numpy import array
from walkers.walker import Walker
from scipy.stats import norm
from scipy import stats


class LowDegreeBiasedWalker(Walker):
    """
    Walker more likely to go to a lower degree node 
    probability is calculated by  (stat of a code)/(sum of stats of all neighbors)
    where stat = 1 - phi(  (node_degree-mean)/std )
    """
    def __init__(self):
        self.neighbor_prob = {}

    def reset(self):
        super().reset()
        self.neighbors_weighted = None

    def load_graph(self, graph):
        super().load_graph(graph)
        degree_dict = { node:degree for node,degree in graph.degree}
        for i in range(len(graph)):
            neighbor_degrees = array([ degree_dict[neighbor] for neighbor in self.neighbors[i] ])
            if len(set(neighbor_degrees)) > 1:
                neighbor_zscore = stats.zscore(neighbor_degrees)
                neighbor_statistics = 1 - norm(loc = 0, scale = 1).cdf(neighbor_zscore)
                sum_neighbor_stat = sum(neighbor_statistics)
                self.neighbor_prob[i] = neighbor_statistics / sum_neighbor_stat

            elif len(self.neighbors[i]) == 0:
                continue

            else:
                self.neighbor_prob[i] = [1/len(self.neighbors[i])] * len(self.neighbors[i])

        self.cur = choice(list(self.graph))

    def move(self):
        self.cur = choice(self.neighbors[self.cur], p = self.neighbor_prob[self.cur])


        