import numpy as np
import matplotlib.pyplot as plt
from graph import Graph
from walkers import RandomWalker
from walkers.greedy_unbiased_walker import GreedyUnbiasedWalker
from walkers.degree_biased_walker import DegreeBiasedWalker
from walkers.low_degree_biased_walker import LowDegreeBiasedWalker
from walkers.no_back_track_walker import NoBackTrackWalker
from utils import largest_comp



class Competition():
    def __init__(self):
        pass
    @staticmethod
    def competition(graph, walker1,walker2, steps):
        walker1.reset()
        walker2.reset()
        walker1.load_graph(graph)
        walker2.load_graph(graph)
        roll = np.random.choice([0,1], size = steps)

        visited1 = {walker1.cur}
        visited2 = {walker2.cur}

        n = len(graph)

        proportions1 = np.ones(steps+1)
        proportions2 = np.ones(steps+1)

        for step in range(steps):
            if roll[step] == 0:
                walker1.move()
                if walker1.cur not in visited1 and walker1.cur not in visited2:
                    visited1.add(walker1.cur)
                    proportions1[step+1] = proportions1[step] + 1
                else:
                    proportions1[step+1] = proportions1[step] 

                walker2.move()
                if walker2.cur not in visited1 and walker2.cur not in visited2:
                    visited2.add(walker2.cur)
                    proportions2[step+1] = proportions2[step] + 1
                else:
                    proportions2[step+1] = proportions2[step] 
            else:
                walker2.move()
                if walker2.cur not in visited1 and walker2.cur not in visited2:
                    visited2.add(walker2.cur)
                    proportions2[step+1] = proportions2[step] + 1
                else:
                    proportions2[step+1] = proportions2[step] 
                
                walker1.move()
                if walker1.cur not in visited1 and walker1.cur not in visited2:
                    visited1.add(walker1.cur)
                    proportions1[step+1] = proportions1[step] + 1
                else:
                    proportions1[step+1] = proportions1[step] 

        return {'proportion_1':proportions1/n, 'proportion_2':proportions2/n}

    # competition on ERRG
    @staticmethod
    def simulate_competition_on_er(n, d, walk_class1, walk_class2, steps, walk_para1 = None, walk_para2 = None, k=1,return_value =True):
        if not walk_para1:
            walker1 = walk_class1()
        else:
            walker1 = walk_class1(walk_para1)

        if not walk_para2:
            walker2 = walk_class2()
        else:
            walker2 = walk_class2(walk_para2)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        threshold = largest_comp(d) * 0.95
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_er_random_graph(n, d/n)
            results = Competition.competition(graph, walker1, walker2, steps)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= threshold:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_on_er(n, d, walk_class1, walk_class2, steps, walk_para1 = None, walk_para2 = None, k=1,return_value =True):
        results = Competition.simulate_competition_on_er(n, d, walk_class1, walk_class2, steps, 
                                                walk_para1, walk_para2, k=k, return_value = return_value)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')


        plt.title("Proportion of Visited Vertices vs. # of Steps on ERRG with 'k = {:d}, n={:d}, p={:.2f}'".format(k, n, d/n))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return results
                                
    # competition on d_regular
    @staticmethod
    def simulate_competition_on_d_regular(n, d, walk_class1, walk_class2, steps, walk_para1 = None, 
                                            walk_para2 = None, k=1,return_value =True):
        if not walk_para1:
            walker1 = walk_class1()
        else:
            walker1 = walk_class1(walk_para1)

        if not walk_para2:
            walker2 = walk_class2()
        else:
            walker2 = walk_class2(walk_para2)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        threshold = largest_comp(d) * 0.95
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_k_regular_random_graph(d, n)
            results = Competition.competition(graph, walker1, walker2, steps)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= threshold:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_on_d_regular(n, d, walk_class1, walk_class2, steps, walk_para1 = None, walk_para2 = None, k=1,return_value =True):
        results = Competition.simulate_competition_on_d_regular(n, d, walk_class1, walk_class2, steps, 
                                                walk_para1, walk_para2, k=k, return_value = return_value)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')


        plt.title("Proportion of Visited Vertices vs. # of Steps on d_regular with 'k = {:d}, n={:d}, d={:d}'".format(k, n, d))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return results

    # competition of FDP
    @staticmethod
    def simulate_competition_on_fdp(n, d_p, walk_class1, walk_class2, steps, walk_para1 = None, 
                                            walk_para2 = None, k=1,return_value =True):
        if not walk_para1:
            walker1 = walk_class1()
        else:
            walker1 = walk_class1(walk_para1)

        if not walk_para2:
            walker2 = walk_class2()
        else:
            walker2 = walk_class2(walk_para2)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        d_seq = Graph.get_rg_degree_proportion_sequence_gen(n,d_p)
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_rg_degree_distribution(d_seq)
            results = Competition.competition(graph, walker1, walker2, steps)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= 0.5:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_on_fdp(n, d_p, walk_class1, walk_class2, steps, walk_para1 = None, walk_para2 = None, k=1,return_value =True):
        results = Competition.simulate_competition_on_fdp(n, d_p, walk_class1, walk_class2, steps, 
                                                walk_para1, walk_para2, k=k, return_value = return_value)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')


        plt.title("Proportion of Visited Vertices vs. # of Steps on FDP with 'k = {:d}, n={:d}, d_p={}'".format(k, n, d_p))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return results

    # competition of EDP
    @staticmethod
    def simulate_competition_on_edp(n, d_p, walk_class1, walk_class2, steps, walk_para1 = None, 
                                            walk_para2 = None, k=1,return_value =True):
        if not walk_para1:
            walker1 = walk_class1()
        else:
            walker1 = walk_class1(walk_para1)

        if not walk_para2:
            walker2 = walk_class2()
        else:
            walker2 = walk_class2(walk_para2)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_expected_d_random_graph(n, d_p)
            results = Competition.competition(graph, walker1, walker2, steps)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= 0.5:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_on_edp(n, d_p, walk_class1, walk_class2, steps, walk_para1 = None, walk_para2 = None, k=1,return_value =True):
        results = Competition.simulate_competition_on_edp(n, d_p, walk_class1, walk_class2, steps, 
                                                walk_para1, walk_para2, k=k, return_value = return_value)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')


        plt.title("Proportion of Visited Vertices vs. # of Steps on EDP with 'k = {:d}, n={:d}, d_p={}'".format(k, n, d_p))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return results


    # competition on BA(preferential attachment)
    def simulate_competition_on_ba(n,m, walk_class1, walk_class2, steps, walk_para1 = None, 
                                            walk_para2 = None, k=1,return_value =True):
        if not walk_para1:
            walker1 = walk_class1()
        else:
            walker1 = walk_class1(walk_para1)

        if not walk_para2:
            walker2 = walk_class2()
        else:
            walker2 = walk_class2(walk_para2)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_BA_model_graph(n, m)
            results = Competition.competition(graph, walker1, walker2, steps)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= 0.5:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_on_ba(n, m, walk_class1, walk_class2, steps, walk_para1 = None, walk_para2 = None, k=1,return_value =True):
        results = Competition.simulate_competition_on_ba(n, m, walk_class1, walk_class2, steps, 
                                                walk_para1, walk_para2, k=k, return_value = return_value)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')


        plt.title("Proportion of Visited Vertices vs. # of Steps on EDP with 'k = {:d}, n={:d}, d_p={}'".format(k, n, d_p))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return results


