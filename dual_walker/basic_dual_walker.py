from abc import ABC, abstractmethod


class DualWalker(ABC):
    """
    Abstract class for a walker on a graph
    """

    def load_graph(self, graph):
        self.graph = graph
        self.neighbors = {node: list(neighbors.keys()) for node, neighbors in self.graph.adj.items()}
        self.cur1 = None
        self.cur2 = None

    def reset(self):
        self.graph = None
        self.neighbors = None
        self.cur1 = None
        self.cur2 = None

    @abstractmethod
    def move(self):
        """
        Moves the walker to the next node in the graph given a strategy
        """
        pass

    

    def get_m_length_neighbor(self, node, length):
        '''
        return all the neighbors with length less than or equal to a number
        '''
        neighbors_cur = set(self.neighbors[node])
        if length == 1:
            return neighbors_cur
        else:
            for i in range(length-1):
                adding = {new_neighbor  for neighbor in neighbors_cur for new_neighbor in self.neighbors[neighbor]}
                neighbors_cur = adding + neighbors_cur
            
            return neighbors_cur

    def get_dist_neighbor_dict(self, node, max_dist):
        '''
        A breadth first search for neighbors with different distances 
        '''
        if max_dist <= 1:
            raise ValueError('max_length should be at least 2')
        else: 
            cur_shell = self.neighbors[node]
            visited = set(cur_shell)
            dist_neighbor = {1:visited}
            

            for i in range(max_dist-1):
                cur_dist = i+2 
                next_shell = {new_neighbor for neighbor in cur_shell for new_neighbor in self.neighbors[neighbor]} - visited
                dist_neighbor[cur_dist] = next_shell

                visited = visited.union(next_shell)
                cur_shell = next_shell
            
            return dist_neighbor
