import networkx as nx

class Graph:

    @staticmethod
    def get_er_random_graph(n : int, p : float):
        return nx.gnp_random_graph(n, p)
    
    @staticmethod 
    def get_er_random_graph_fast(n: int, p: float):
        return nx.fast_gnp_random_graph(n,p)

    @staticmethod
    def get_k_regular_random_graph(d: int, n: int):
        return nx.random_regular_graph(d, n)

    @staticmethod
    def get_rg_degree_proportion_sequence(n: int, d: int, d1: int, d2: int):
        '''
        return a degree sequence for a given n and the two possible degrees 
        degree of each node is either d1 or d2
        The goal is to produce a sequence compatible with the random_degree_sequence_graph func
        The random_degree_sequence_graph does not always guarantee a graph, default number of tries is 10
        
        implement the feasibility check
        '''
        # check order
        
        if d1 >= d or  d >= d2:
            raise nx.NetworkXUnfeasible
        
        delta = (d2-d)/(d2-d1)
        count_d1 = round(n*delta)
        count_d2 = n - count_d1

        # check feasibility 
        if (count_d1 * d1 + count_d2 * d2)%2 == 1:
            count_d2 += 1
            count_d1 += -1
        if min(count_d1,count_d2) <= d2:
            raise nx.NetworkXUnfeasible

        d_seq = [d2] * count_d2 + [d1] * count_d1

        return d_seq

    
    @staticmethod
    def get_rg_degree_distribution(d_seq):
        return nx.random_degree_sequence_graph(d_seq)
        
