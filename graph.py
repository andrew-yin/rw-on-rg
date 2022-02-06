import networkx as nx

class Graph:

    @staticmethod
    def get_er_random_graph(n : int, p : float):
        return nx.gnp_random_graph(n, p)