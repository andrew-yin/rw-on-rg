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