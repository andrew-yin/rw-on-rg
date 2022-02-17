import numpy as np
import matplotlib.pyplot as plt

from graph import Graph
from walkers import RandomWalker, GreedyUnbiasedWalker
from utils import largest_comp


class Simulator:

    def __init__(self):
        pass

    @staticmethod
    def simulate_walk(graph, walker, steps, calculate_prop=True):
        walker.reset()
        walker.load_graph(graph)
        n = len(graph)

        walk = [walker.cur]
        proportions = np.ones(steps+1)

        # Simulate walk
        visited = set(walk)
        for i in range(1, steps+1):
            walker.move()
            walk.append(walker.cur)
            if walker.cur not in visited:
                visited.add(walker.cur)
                proportions[i] = proportions[i-1]+1
            else:
                proportions[i] = proportions[i-1]

        # Generate results
        results = {
            'walk': walk,
        }
        if calculate_prop:
            results['proportions'] = proportions/n
        return results

    @staticmethod
    def simulate_rw_on_rg_visited_prop(n, p, k=1, comp_adj=True, d=None):
        """
        Simulate the average proportion of visited vertices over n*log(n)^2 steps
        of a random walk on a random graph over k samples. 

        If comp_adj is true, we exclude simulated runs that do not visit a 
        certain proportion of vertices after n*log(n)^2 steps, as you can
        be fairly certain these simulations do not start in the largest component
        of the graph.
        """
        random_walker = RandomWalker()
        steps = int(n*np.log(n)*np.log(n))
        proportion_sum = np.zeros(steps+1)

        threshold = largest_comp(d) 
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_er_random_graph(n, d/n)
            results = Simulator.simulate_walk(graph, random_walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def simulate_guw_on_rg_visited_prop(n, p, k=1, comp_adj=True, d=None):
        greedy_walker = GreedyUnbiasedWalker()
        steps = int(n*np.log(n)*np.log(n))
        proportion_sum = np.zeros(steps+1)

        threshold = largest_comp(d)
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_er_random_graph(n, p)
            results = Simulator.simulate_walk(
                graph, greedy_walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def plot_rw_on_rg_visited_prop(n, p, k=1, comp_adj=True, d=None):
        proportion_avg = Simulator.simulate_rw_on_rg_visited_prop(
            n, p, k, comp_adj, d)
        steps = len(proportion_avg)-1

        c = np.arange(0, 1, 0.1)*steps
        avg_at_each_c = [proportion_avg[int(i)] for i in c]
        plt.scatter(c, avg_at_each_c, c='r', s=50)
        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, p={:.2f}'.format(k, n, p))
        plt.title("Proportion of Visited Vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
