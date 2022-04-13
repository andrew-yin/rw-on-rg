from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice



class DWRandomGUOTNTB(DualWalker):
    """
    Guo with tie breaker the number of unclaimed nodes in that tree
    """
    def __init__(self,degree = 2):
        self.claimed1 = None
        self.claimed2 = None
        self.degree = degree
        self.past_count = 2

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
        self.tree_nodes_dict = {node:self.get_neighbor_treenodes_dict_with_dist(node, self.degree) for node in self.neighbors.keys()}

        # self.node_dist_neighbor_dict = {node: self.get_dist_neighbor_dict(node, self.degree - 1) for node in self.neighbors.keys()}


    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None


    def move(self,flip):
        

        
        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

            
            count = self.past_count - 1
            while count <= self.degree:
                # if if count is one, just search for the d1 neighbors 
                if count == 1: 
                    not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                    
                    if len(not_claimed) != 0:
                        score_dict = {d1_neighbor: len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict'][d1_neighbor] - self.claimed1 - self.claimed2) 
                                            for d1_neighbor in not_claimed }
                        max_score = max(score_dict.values())
                        self.cur2 = choice([d1_neighbor for d1_neighbor in score_dict.keys() if score_dict[d1_neighbor] == max_score])
                        print(max_score)
                        break
                    else:
                        count += 1 
                # if count is not 1, search for d = count neighbors, stop search if not claimed neighbor is found 
                else:
                    
                    d1_possible = [ d1_neighbor for d1_neighbor in self.neighbors[self.cur2]
                                        if len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict_w_dist'][d1_neighbor][count] - self.claimed1 - self.claimed2) > 0]

                    if len(d1_possible) != 0:
                        score_dict = {d1_neighbor : len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict'][d1_neighbor] - self.claimed1 - self.claimed2) 
                                                            for d1_neighbor in d1_possible}
                        max_score = max(score_dict.values())
                        self.cur2 = choice([d1_neighbor for d1_neighbor in score_dict.keys() if score_dict[d1_neighbor] == max_score])
                        print(max_score)
                        break 
                    else: 
                        count += 1 
            else: 
                self.cur2 = choice(self.neighbors[self.cur2])

            
            
            self.past_count = max([2,count-1])
            self.claimed2.add(self.cur2)
            
            # count control is the same as the gneeral guo 

        if flip == 1: 
            
            count = self.past_count - 1
            while count <= self.degree:
                # if if count is one, just search for the d1 neighbors 
                if count == 1: 
                    not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                    
                    if len(not_claimed) != 0:
                        score_dict = {d1_neighbor: len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict'][d1_neighbor] - self.claimed1 - self.claimed2) 
                                            for d1_neighbor in not_claimed }
                        max_score = max(score_dict.values())
                        self.cur2 = choice([d1_neighbor for d1_neighbor in score_dict.keys() if score_dict[d1_neighbor] == max_score])
                        print(max_score)
                        break
                    else:
                        count += 1 
                # if count is not 1, search for d = count neighbors, stop search if not claimed neighbor is found 
                else:
                    
                    d1_possible = [ d1_neighbor for d1_neighbor in self.neighbors[self.cur2]
                                        if len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict_w_dist'][d1_neighbor][count] - self.claimed1 - self.claimed2) > 0]

                    if len(d1_possible) != 0:
                        score_dict = {d1_neighbor : len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict'][d1_neighbor] - self.claimed1 - self.claimed2) 
                                                            for d1_neighbor in d1_possible}
                        max_score = max(score_dict.values())
                        self.cur2 = choice([d1_neighbor for d1_neighbor in score_dict.keys() if score_dict[d1_neighbor] == max_score])
                        print(max_score)
                        break 
                    else: 
                        count += 1 
            else: 
                self.cur2 = choice(self.neighbors[self.cur2])
            
            
            self.past_count = max([2,count-1])
            self.claimed2.add(self.cur2)



            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)
        
        
        
