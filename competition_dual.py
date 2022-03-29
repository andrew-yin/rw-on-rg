
from dual_walker.dual_walker_random_greedy_omniscient import DWRandomGreedyOmniscient
from dual_walker.dual_walker_scouting_greedy_omniscient import DWRandomScoutingGreedy
from dual_walker.dual_walker_low_length_pref_greedy import DWRandomLowLenPrefGreedy
from dual_walker.dual_walker_rw_no_back_track import DWRandomNoBackTrack
from dual_walker.dual_walker_rw_low_degree_preferred import DWRandomLowDegreePreferred
from dual_walker.dual_walker_high_degree_preferred import DWRandomHighDegreePreferred
from dual_walker.dual_walker_rw_switch_llpg_ldp import DWRandomSwitchLLPGtoLDP
from dual_walker.dual_walker_rw_switch_llpg_guo import DWRandomSwitchLLPGtoGUO
from dual_walker.dual_walker_rw_degree_two_guo import DWRandomDegree2GUO
from dual_walker.dual_walker_rw_switch_llpg_2dguo import DWRandomSwitchLLPGto2dGUO
from dual_walker.dual_walker_rw_degree_three_guo import DWRandomDegree3GUO
from dual_walker.dual_walker_rw_general_guo import DWRandomGeneralGUO
from dual_walker.dual_walker_rw_general_guo_optimized import DWRandomGeneralGUORevised
import numpy as np
import matplotlib.pyplot as plt
from graph import Graph
from utils import largest_comp

class CompetitionDual():
    def __init__(self):
        pass
    @staticmethod
    def competition_dual(graph,dual_walker,steps, switch_walker = False, cut_proportion = 0):
        n=len(graph)
        dual_walker.reset()
        dual_walker.load_graph(graph)

        claimed1 = {dual_walker.cur1}
        claimed2 = {dual_walker.cur2}

        proportions1 = np.ones(steps+1)
        proportions2 = np.ones(steps+1)

        flips = np.random.choice([0,1], size = steps)

        if switch_walker:
            real_cut = cut_proportion * n
            reach_cut = False
            for step in range(steps):
                dual_walker.move(flips[step], reach_cut)
                if dual_walker.cur1 not in claimed1 and dual_walker.cur1 not in claimed2:
                    claimed1.add(dual_walker.cur1)
                    proportions1[step+1] = proportions1[step] +1
                else:
                    proportions1[step+1] = proportions1[step]
                
                if dual_walker.cur2 not in claimed1 and dual_walker.cur2 not in claimed2:
                    claimed2.add(dual_walker.cur2)
                    proportions2[step+1] = proportions2[step] +1
                else:
                    proportions2[step+1] = proportions2[step]
                
                if proportions2[step+1] >= real_cut:
                    reach_cut = True

        else:
            for step in range(steps):
                dual_walker.move(flips[step])
                if dual_walker.cur1 not in claimed1 and dual_walker.cur1 not in claimed2:
                    claimed1.add(dual_walker.cur1)
                    proportions1[step+1] = proportions1[step] +1
                else:
                    proportions1[step+1] = proportions1[step]
                
                if dual_walker.cur2 not in claimed1 and dual_walker.cur2 not in claimed2:
                    claimed2.add(dual_walker.cur2)
                    proportions2[step+1] = proportions2[step] +1
                else:
                    proportions2[step+1] = proportions2[step]

        return {'proportion_1':proportions1/n, 'proportion_2':proportions2/n}

    # on er
    @staticmethod
    def simulate_competition_dual_on_er(n,d,steps,dual_walker_class,walker_para = None,k=1, switch_walker = False, cut_proportion = 0):
        if not walker_para:
            dual_walker = dual_walker_class()
        else:
            dual_walker = dual_walker_class(walker_para)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        valid_samples = 0
        threshold = largest_comp(d) * 0.85
        while valid_samples < k:
            graph = Graph.get_er_random_graph(n, d/n)
            results = CompetitionDual.competition_dual(graph, dual_walker, steps, 
                                                        switch_walker = switch_walker,cut_proportion = cut_proportion)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= threshold:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_dual_on_er(n, d, steps, dual_walker_class, walker_para = None, k=1,return_value =True,switch_walker = False, cut_proportion = 0):
        results = CompetitionDual.simulate_competition_dual_on_er(n, d,  steps, dual_walker_class,
                                                walker_para, k=k, switch_walker = switch_walker,cut_proportion = cut_proportion)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')
        plt.title('''Proportion of Visited Vertices vs. # of Steps on ERRG with 
        k = {:d}, n={:d}, p={:.2f}, ratio ={:.6f}'''.format(k, n, d/n, walk1[-1]/walk2[-1]))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of claimed area")
        plt.legend()
        plt.show()
        if return_value:
            return results

    # on d regular
    @staticmethod 
    def simulate_competition_dual_on_d_regular(n,d,steps,dual_walker_class,walker_para = None, k = 1, switch_walker = False, cut_proportion = 0):
        if not walker_para:
            dual_walker = dual_walker_class()
        else:
            dual_walker = dual_walker_class(walker_para)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        valid_samples = 0
        threshold = largest_comp(d) * 0.95
        while valid_samples < k:
            graph = Graph.get_k_regular_random_graph(d, n)
            results = CompetitionDual.competition_dual(graph, dual_walker, steps,
                                                            switch_walker = switch_walker,cut_proportion = cut_proportion)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= threshold:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_dual_on_d_regular(n, d, steps, dual_walker_class, walker_para = None, k=1,return_value =True, switch_walker = False, cut_proportion = 0):
        results = CompetitionDual.simulate_competition_dual_on_d_regular(n, d,  steps, dual_walker_class, walker_para, 
                                                                            k=k, switch_walker = switch_walker,cut_proportion = cut_proportion)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')
        plt.title('''Proportion of Visited Vertices vs. # of Steps on d_regular with 
        k = {:d}, n={:d}, d={:d}, ratio ={:.6f}'''.format(k, n, d, walk1[-1]/walk2[-1]))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of claimed area")
        plt.legend()
        plt.show()
        if return_value:
            return results

    # on fdp
    @staticmethod
    def simulate_competition_dual_on_fdp(n,d_p,steps,dual_walker_class, walker_para=None, k=1, switch_walker = False, cut_proportion = 0):
        if not walker_para:
            dual_walker = dual_walker_class()
        else:
            dual_walker = dual_walker_class(walker_para)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        valid_samples = 0
        d_seq = Graph.get_rg_degree_proportion_sequence_gen(n,d_p)
        while valid_samples < k:
            graph = Graph.get_rg_degree_distribution(d_seq)
            results = CompetitionDual.competition_dual(graph, dual_walker, steps, switch_walker = switch_walker,cut_proportion = cut_proportion)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= 0.5:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_dual_on_fdp(n,d_p,steps,dual_walker_class, walker_para=None, k=1, return_value = True, switch_walker = False, cut_proportion = 0):
        results = CompetitionDual.simulate_competition_dual_on_fdp(n, d_p,  steps, dual_walker_class, walker_para, 
                                                                            k=k, switch_walker = switch_walker,cut_proportion = cut_proportion)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')
        plt.title('''Proportion of Visited Vertices vs. # of Steps on fdp with 
        k = {:d}, n={:d}, d={:d}, d_p ={}, ratio ={:.6f}'''.format(k, n, d_p, walk1[-1]/walk2[-1]))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of claimed area")
        plt.legend()
        plt.show()
        if return_value:
            return results

    # on ba
    @staticmethod
    def simulate_compettion_dual_on_ba(n,m,steps,dual_walker_class, walker_para = None, k = 1,switch_walker = False, cut_proportion = 0):
        if not walker_para:
            dual_walker = dual_walker_class()
        else:
            dual_walker = dual_walker_class(walker_para)

        proportion_sum1 = np.zeros(steps+1)
        proportion_sum2 = np.zeros(steps+1)

        valid_samples = 0
        d_seq = Graph.get_BA_model_graph(n,m)
        while valid_samples < k:
            graph = Graph.get_rg_degree_distribution(d_seq)
            results = CompetitionDual.competition_dual(graph, dual_walker, steps, switch_walker = switch_walker, cut_proportion = cut_proportion)
            proportion1, proportion2 = results['proportion_1'], results['proportion_2']

            if proportion1[-1] + proportion2[-1] >= 0.5:
                proportion_sum1 += proportion1
                proportion_sum2 += proportion2
                valid_samples += 1

        return {'proportion_avg_1': proportion_sum1/k, 
                'proportion_avg_2': proportion_sum2/k, 
                'proportion_avg_total':(proportion_sum1+proportion_sum2)/k}

    @staticmethod
    def plot_competition_dual_on_ba(n, m,steps,dual_walker_class, walker_para=None, k=1, return_value = True, switch_walker = False, cut_proportion = 0):
        results = CompetitionDual.simulate_competition_dual_on_ba(n, m,  steps, dual_walker_class, walker_para, 
                                                                            k=k, switch_walker = switch_walker,cut_proportion = cut_proportion)
        
        walk1,walk2,walk_total = results['proportion_avg_1'], results['proportion_avg_2'], results['proportion_avg_total']

        x = np.arange(1,len(walk1)+1, step = 1)
        plt.plot(x,walk1, label = 'walker1')
        plt.plot(x,walk2, label = 'walker2')
        plt.plot(x,walk_total, label = 'total')
        plt.title('''Proportion of Visited Vertices vs. # of Steps on fdp with 
        k = {:d}, n={:d}, m={:d}, ratio ={:.6f}'''.format(k, n, m, walk1[-1]/walk2[-1]))
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of claimed area")
        plt.legend()
        plt.show()
        if return_value:
            return results

