from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice

class DWRandomGeneralGUO(DualWalker):
    """
    General GUO
    """
    def __init__(self,degree = 1):
        self.claimed1 = None
        self.claimed2 = None
        self.degree = degree

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


    def get_m_length_neighbor(self, node, length):
        return super().get_m_length_neighbor(node = node,length = length)

    def move(self,flip):
        
        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)

            
            count = 1 
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
                                        if len( self.get_m_length_neighbor(d1_neighbor,count - 1) - self.claimed1 - self.claimed2) > 0]
                    if len(d1_possible) != 0:
                        self.cur2 = choice(tuple(d1_possible))
                        break 
                    else: 
                        count += 1 
            else: 
                self.cur2 = choice(self.neighbors[self.cur2])

            self.claimed2.add(self.cur2)    


        if flip == 1: 
            count = 1 
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
                                        if len( self.get_m_length_neighbor(d1_neighbor,count - 1) - self.claimed1 - self.claimed2) > 0]
                    if len(d1_possible) != 0:
                        self.cur2 = choice(tuple(d1_possible))
                        break 
                    else: 
                        count += 1 
            else: 
                self.cur2 = choice(self.neighbors[self.cur2])
            self.claimed2.add(self.cur2) 



            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)
        