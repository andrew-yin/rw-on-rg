import networkx as nx
import math

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
    def get_rg_degree_proportion_sequence_gen(n: int, d_p: dict):
        '''
        take a dictionary of desired degree distribution in the format {degree:proportion}
        return a sequence with lenth n that roughly agree with the degree distribution and is always graphible
        '''

        d_list = list(d_p.keys())
        d_list.sort(reverse=True)

        p_list = [d_p[d] for d in d_list]
        if abs(sum(p_list)-1) >=0.001:
            raise ValueError('probabilities should add up to one')

        count_list = [round(n*p) for p in p_list[:-1]]
        last_count = n - sum(count_list)
        count_list.append(last_count)

        least_odd_indice = None
        least_even_indice = None
        cur_indice = -1
        while (least_odd_indice == None or least_even_indice == None) and cur_indice >= -len(d_p):
            if d_list[cur_indice]%2 == 1:
                if least_odd_indice != None:
                    cur_indice += -1
                else:
                    least_odd_indice = cur_indice
                    cur_indice += -1
            else:
                if least_even_indice != None:
                    cur_indice += -1
                else:
                    least_even_indice = cur_indice
                    cur_indice += -1

        # even check
        total = 0
        for i in range(len(d_list)):
            total += d_list[i] * count_list[i]
        if total%2 == 1:
            count_list[least_odd_indice] += 1
            count_list[least_even_indice] += -1

        #feasibility check
        if min(count_list) <= d_list[1]:
            raise ValueError('n too small')
        

        d_seq = []
        for i in range(len(d_list)):
            d_seq = d_seq + [d_list[i]] * count_list[i]
        return d_seq
    
    @staticmethod
    def get_rg_degree_distribution(d_seq):
        return nx.random_degree_sequence_graph(d_seq)
        
    @staticmethod
    def get_BA_model_graph(n:int, m:int):
        return nx.barabasi_albert_graph(n,m)

     # This method generates graphs with an expected degree of d
    @staticmethod
    def get_expected_d_random_graph(n: int, d_p: dict):
        # n- total number of nodes, d: a list of degrees
        d_list = list(d_p.keys())
        d_list.sort(reverse=True)

        p_list = [d_p[d] for d in d_list]

        count_list = [round(n*p) for p in p_list[:-1]]
        last_count = n - sum(count_list)
        count_list.append(last_count)
        
        d_seq = []
        for i in range(len(d_list)):
            d_seq = d_seq + [d_list[i]] * count_list[i]
        return nx.expected_degree_graph(d_seq)

    @staticmethod
    def get_largest_comp_size(graph):
        '''
        return the size of the largest component
        '''
        size_list = [ len(component) for component in sorted(nx.connected_components(graph), key=len, reverse=True) ]
        return size_list[0]
