import networkx as nx
import math

class Graph:

    @staticmethod
    def get_er_random_graph(n : int, p : float):
        return nx.gnp_random_graph(n, p)

    @staticmethod
    def get_k_regular_random_graph(d: int, n: int):
        return nx.random_regular_graph(d, n)

    # This method generates graphs with an expected degree of d
    @staticmethod
    def get_expected_d_random_graph(d: [], p: [], n: int):
        # n- total number of nodes, d: a list of degrees
        z1, z2 = [], []
        for i in range(math.ceil(p[0]*n)):
            z1.append(d[0])
        for i in range(math.floor(p[1]*n)):
            z2.append(d[1])
        z = z1+z2
        # expected_d = d[0]*p[0] + d[1]*p[1]
        return nx.expected_degree_graph(z)
