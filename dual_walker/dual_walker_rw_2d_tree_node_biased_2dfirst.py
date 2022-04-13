from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice

class DWRandom2dTreeNodeBiasedD2first(DualWalker):
    """
    Logic explained:
    The agent will determine 2 steps at once. The highest priority is given to 2 consecutive unclaimed nodes. If no such paths are available, 
    the agent will choose a path with an unclaimed second node. In cases of a tie, a path with more equivalent neighbors are prefered (deterministic)
    oo > xo > ox > xx
    """
    def __init__(self):
        self.claimed1 = None
        self.claimed2 = None
        self.future2 = -1 

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

    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None


    def move(self,flip):

        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

            if self.future2 != -1: 
                self.cur2 = self.future2
                self.future2 = -1
            else:   
                all_length2_unclaimed_d2 = { d1neighbor: [d2neighbor for d2neighbor in self.neighbors[d1neighbor] if d2neighbor not in self.claimed1.union(self.claimed2)] 
                                                            for d1neighbor in self.neighbors[self.cur2]
                                                            if len(set(self.neighbors[d1neighbor]) - self.claimed1 - self.claimed2) != 0 }

                if len(all_length2_unclaimed_d2.keys()) == 0:
                    not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                    if len(not_claimed) != 0:
                        self.cur2 = choice(tuple(not_claimed))
                    else:
                        self.cur2 = choice(self.neighbors[self.cur2])

                else:
                    all_length2_unclaimed_d1d2 = { d1neighbor:all_length2_unclaimed_d2[d1neighbor] for d1neighbor in all_length2_unclaimed_d2.keys() 
                                                    if d1neighbor not in self.claimed1.union(self.claimed2)}

                    if len(all_length2_unclaimed_d1d2.keys()) == 0:
                        d1_score_dict = { d1neighbor: len(all_length2_unclaimed_d2[d1neighbor]) for d1neighbor in all_length2_unclaimed_d2.keys()}
                        max_score = max(d1_score_dict.values())
                        self.cur2 = choice( [d1neighbor for d1neighbor in d1_score_dict.keys() if d1_score_dict[d1neighbor] == max_score] )
                        self.future2 = choice( all_length2_unclaimed_d2[self.cur2] )

                    else:
                        d1_score_dict = { d1neighbor: len(all_length2_unclaimed_d1d2[d1neighbor]) for d1neighbor in all_length2_unclaimed_d1d2.keys()}
                        max_score = max(d1_score_dict.values())
                        self.cur2 = choice( [d1neighbor for d1neighbor in d1_score_dict.keys() if d1_score_dict[d1neighbor] == max_score] )
                        self.future2 = choice( all_length2_unclaimed_d1d2[self.cur2] )

            
            self.claimed2.add(self.cur2)    






        if flip == 1: 

            if self.future2 != -1: 
                self.cur2 = self.future2
                self.future2 = -1
            else:   
                all_length2_unclaimed_d2 = { d1neighbor: [d2neighbor for d2neighbor in self.neighbors[d1neighbor] if d2neighbor not in self.claimed1.union(self.claimed2)] 
                                                            for d1neighbor in self.neighbors[self.cur2]
                                                            if len(set(self.neighbors[d1neighbor]) - self.claimed1 - self.claimed2) != 0 }

                if len(all_length2_unclaimed_d2.keys()) == 0:
                    not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                    if len(not_claimed) != 0:
                        self.cur2 = choice(tuple(not_claimed))
                    else:
                        self.cur2 = choice(self.neighbors[self.cur2])

                else:
                    all_length2_unclaimed_d1d2 = { d1neighbor:all_length2_unclaimed_d2[d1neighbor] for d1neighbor in all_length2_unclaimed_d2.keys() 
                                                    if d1neighbor not in self.claimed1.union(self.claimed2)}

                    if len(all_length2_unclaimed_d1d2.keys()) == 0:
                        d1_score_dict = { d1neighbor: len(all_length2_unclaimed_d2[d1neighbor]) for d1neighbor in all_length2_unclaimed_d2.keys()}
                        max_score = max(d1_score_dict.values())
                        self.cur2 = choice( [d1neighbor for d1neighbor in d1_score_dict.keys() if d1_score_dict[d1neighbor] == max_score] )
                        self.future2 = choice( all_length2_unclaimed_d2[self.cur2] )

                    else:
                        d1_score_dict = { d1neighbor: len(all_length2_unclaimed_d1d2[d1neighbor]) for d1neighbor in all_length2_unclaimed_d1d2.keys()}
                        max_score = max(d1_score_dict.values())
                        self.cur2 = choice( [d1neighbor for d1neighbor in d1_score_dict.keys() if d1_score_dict[d1neighbor] == max_score] )
                        self.future2 = choice( all_length2_unclaimed_d1d2[self.cur2] )

            self.claimed2.add(self.cur2)  

            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)