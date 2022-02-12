from abc import ABC, abstractmethod


class Walker(ABC):
    """
    Abstract class for a walker on a graph
    """

    def load_graph(self, graph):
        self.graph = graph
        self.neighbors = {node: list(neighbors.keys()) for node, neighbors in self.graph.adj.items()}
        self.cur = None

    def reset(self):
        self.graph = None
        self.neighbors = None
        self.cur = None

    @abstractmethod
    def move(self):
        """
        Moves the walker to the next node in the graph given a strategy
        """
        pass
