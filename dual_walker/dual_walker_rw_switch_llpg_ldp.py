from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice
from numpy import array
from scipy.stats import norm, zscore
from networkx import shortest_path_length

class DWRandomSwitchLLPGtoLDP(DualWalker):
    """
    Agent first adopt a LLPG, and switch to ldp when the claimed proportion hit a cut
    """
    def __init__(self):
        self.claimed1 = None
        self.claimed2 = None
        self.neighbor_prob = {}

    def load_graph(self, graph):
        super().load_graph(graph)
        self.cur1 = choice(list(self.graph))
        while len(self.neighbors[self.cur1]) == 0:
            self.cur1 = choice(list(self.graph))
        self.claimed1 = {self.cur1}

        self.cur2 = choice(list(self.graph))
        while len(self.neighbors[self.cur2]) == 0:
            self.cur2 = choice(list(self.graph))
        self.claimed2 = {self.cur2}

        #construct the propability dict
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


    def move(self,flip,reach_cut):
        if not reach_cut:
            if flip == 0:
                self.cur1 = choice(self.neighbors[self.cur1]) 
                self.claimed1.add(self.cur1)


                not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                if len(not_claimed) != 0:
                    length2rw = {node:shortest_path_length(self.graph,node,self.cur1) for node in list(not_claimed)}
                    min_len = min(list(length2rw.values()))
                    self.cur2 = choice( [node for node in length2rw if length2rw[node] == min_len] )

                else:
                    length2rw = {node:shortest_path_length(self.graph,node,self.cur1) for node in self.neighbors[self.cur2]}
                    min_len = min(list(length2rw.values()))
                    self.cur2 = choice( [node for node in length2rw if length2rw[node] == min_len] )

                self.claimed2.add(self.cur2)


            if flip == 1: 
                not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                if len(not_claimed) != 0:
                    length2rw = {node:shortest_path_length(self.graph,node,self.cur1) for node in list(not_claimed)}
                    min_len = min(list(length2rw.values()))
                    self.cur2 = choice( [node for node in length2rw if length2rw[node] == min_len] )

                else:
                    length2rw = {node:shortest_path_length(self.graph,node,self.cur1) for node in self.neighbors[self.cur2]}
                    min_len = min(list(length2rw.values()))
                    self.cur2 = choice( [node for node in length2rw if length2rw[node] == min_len] )
                    
                self.claimed2.add(self.cur2)  

                self.cur1 = choice(self.neighbors[self.cur1]) 
                self.claimed1.add(self.cur1)
        
        else:
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