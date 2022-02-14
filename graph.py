import networkx as nx

class Graph:

    @staticmethod
    def get_er_random_graph(n : int, p : float):
        return nx.gnp_random_graph(n, p)

    @staticmethod
    def get_k_regular_random_graph(d: int, n: int):
        return nx.random_regular_graph(d, n)
