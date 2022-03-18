from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice
from networkx import shortest_path_length

class DWRandomScoutingGreedy(DualWalker):
    """
    The greedy agent will try to first get close to the the random walker
    Once the agent is 2 steps away from the random walker, it will starts to perform greedy walk 
    Note: since the diameter of our graph (1000n) is not large, this strategy seems to be a very mild upgrade to guo
    """
    def __init__(self):
        self.claimed1 = None
        self.claimed2 = None
        self.find = False

    def load_graph(self, graph):
        super().load_graph(graph)
        self.cur1 = choice(list(self.graph))
        self.claimed1 = {self.cur1}

        self.cur2 = choice(list(self.graph))
        self.claimed2 = {self.cur2}

    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None


    def move(self,flip):
        if self.find:
            if flip == 0:
                self.cur1 = choice(self.neighbors[self.cur1]) 
                self.claimed1.add(self.cur1)

                not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                if len(not_claimed) != 0: 
                    self.cur2 = choice(tuple(not_claimed))
                else:
                    self.cur2 = choice(self.neighbors[self.cur2])
                self.claimed2.add(self.cur2)    

            if flip == 1: 
                not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                if len(not_claimed) != 0: 
                    self.cur2 = choice(tuple(not_claimed))
                else:
                    self.cur2 = choice(self.neighbors[self.cur2])
                self.claimed2.add(self.cur2) 

                self.cur1 = choice(self.neighbors[self.cur1]) 
                self.claimed1.add(self.cur1)

        
        else:
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


                if min_len <= 2:
                    self.find = True
                self.claimed2.add(self.cur2)

            else:
                
                not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                if len(not_claimed) != 0:
                    length2rw = {node:shortest_path_length(self.graph,node,self.cur1) for node in list(not_claimed)}
                    min_len = min(list(length2rw.values()))
                    self.cur2 = choice( [node for node in length2rw if length2rw[node] == min_len] )

                else:
                    length2rw = {node:shortest_path_length(self.graph,node,self.cur1) for node in self.neighbors[self.cur2]}
                    min_len = min(list(length2rw.values()))
                    self.cur2 = choice( [node for node in length2rw if length2rw[node] == min_len] )


                if min_len <= 2:
                    self.find = True
                self.claimed2.add(self.cur2)


                self.cur1 = choice(self.neighbors[self.cur1]) 
                self.claimed1.add(self.cur1)

                