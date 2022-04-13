from dual_walker.basic_dual_walker import DualWalker
from numpy.random import choice



class DWRandomPPTNTB(DualWalker):
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
        self.paths = {node: self.get_all_path(node, self.degree) for node in self.neighbors.keys()}
        self.path_score_list = self.get_path_score_list(self.degree)

        # self.node_dist_neighbor_dict = {node: self.get_dist_neighbor_dict(node, self.degree - 1) for node in self.neighbors.keys()}


    def reset(self):
        super().reset()
        self.claimed1 = None
        self.claimed2 = None


    def move(self,flip):
        

        
        if flip == 0:
            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)


            path_score_pair_list = [(path, self.get_path_score(path, self.claimed1.union(self.claimed2), self.path_score_list)) 
                                    for path in self.paths[self.cur2] 
                                    if self.get_path_score(path, self.claimed1.union(self.claimed2), self.path_score_list) > 0 ]

            if len(path_score_pair_list) == 0:
                self.cur2 = choice(self.neighbors[self.cur2])
            else:
                # this score is for path 
                max_score = max( [ score for path,score in path_score_pair_list])
                d1_possible = [ path[1] for path,score in path_score_pair_list if score == max_score ]
                

                tb_score = {d1_neighbor : len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict'][d1_neighbor] - self.claimed1 - self.claimed2) 
                                                            for d1_neighbor in d1_possible}

                max_tb_score = max(tb_score.values())
                
                self.cur2 = choice([d1_neighbor for d1_neighbor in tb_score.keys() if tb_score[d1_neighbor] == max_tb_score])
                
            
            self.claimed2.add(self.cur2)
            


        if flip == 1: 
            
            path_score_pair_list = [(path, self.get_path_score(path, self.claimed1.union(self.claimed2), self.path_score_list)) 
                                    for path in self.paths[self.cur2] 
                                    if self.get_path_score(path, self.claimed1.union(self.claimed2), self.path_score_list) > 0 ]

            if len(path_score_pair_list) == 0:
                self.cur2 = choice(self.neighbors[self.cur2])
            else:
                max_score = max( [ score for path,score in path_score_pair_list])
                d1_possible = [ path[1] for path,score in path_score_pair_list if score == max_score ]
                

                tb_score = {d1_neighbor : len( self.tree_nodes_dict[self.cur2]['neighbor_treenodes_dict'][d1_neighbor] - self.claimed1 - self.claimed2) 
                                                            for d1_neighbor in d1_possible}

                max_tb_score = max(tb_score.values())
                
                self.cur2 = choice([d1_neighbor for d1_neighbor in tb_score.keys() if tb_score[d1_neighbor] == max_tb_score])
            
            self.claimed2.add(self.cur2)



            self.cur1 = choice(self.neighbors[self.cur1]) 
            self.claimed1.add(self.cur1)