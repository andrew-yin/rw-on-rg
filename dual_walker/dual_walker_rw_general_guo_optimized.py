from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice


class DWRandomGeneralGUORevised(DualWalker):
    """
    General GUO
    """
    def __init__(self,degree = 1):
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
        self.node_dist_neighbor_dict = {node: self.get_dist_neighbor_dict(node, self.degree - 1) for node in self.neighbors.keys()}


    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None


    def get_m_length_neighbor(self, node, length):
        return super().get_m_length_neighbor(node = node,length = length)

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
                        self.cur2 = choice(tuple(not_claimed))
                        break
                    else:
                        count += 1 
                # if count is not 1, search for d = count neighbors, stop search if not claimed neighbor is found 
                else:
                    d1_possible = [ d1_neighbor for d1_neighbor in self.neighbors[self.cur2]
                                        if len( self.node_dist_neighbor_dict[d1_neighbor][count-1] - self.claimed1 - self.claimed2) > 0]
                    if len(d1_possible) != 0:
                        self.cur2 = choice(tuple(d1_possible))
                        break 
                    else: 
                        count += 1 
            else: 
                self.cur2 = choice(self.neighbors[self.cur2])
                
            
            self.past_count = max([2,count])
            self.claimed2.add(self.cur2)    
            # count control: if the count k <= degree, then this means that the closest unclaimed node is k steps way, and there's no unclaimed node with
            # distance less than or equal to k - 1. Now when the agent move to the new node, the cloest unclaimed node has distance k - 1 since if an
            # unclaimed node is closer than that, it will be at most k-1 steps away from the previous position. Therefore, we can start the search 
            # from count = k - 1. If the final count > degree (ie the while loop is finishes), then no unclaimed node is within d steps => the closest 
            # unclaimed node is at least d + 1 steps away. After the agent move, an unclaimed node has a distance at least d since ow it will have distance 
            # d to the previous position   

        if flip == 1: 

            count = self.past_count - 1 
            while count <= self.degree:
                if count == 1: 
                    not_claimed = set(self.neighbors[self.cur2]) - self.claimed1 - self.claimed2
                    
                    if len(not_claimed) != 0:
                        self.cur2 = choice(tuple(not_claimed))
                        break
                    else:
                        count += 1 
                else:
                    d1_possible = [ d1_neighbor for d1_neighbor in self.neighbors[self.cur2]
                                        if len( self.node_dist_neighbor_dict[d1_neighbor][count-1] - self.claimed1 - self.claimed2) > 0]
                    if len(d1_possible) != 0:
                        self.cur2 = choice(tuple(d1_possible))
                        break 
                    else: 
                        count += 1 
            else: 
                self.cur2 = choice(self.neighbors[self.cur2])
                
        

            self.past_count = max([2,count])
            self.claimed2.add(self.cur2) 



            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

