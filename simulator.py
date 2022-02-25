
import numpy as np
import matplotlib.pyplot as plt
from graph import Graph
from walkers import RandomWalker, GreedyUnbiasedWalker, DegreeBiasedWalker
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
    def simulate_w_on_rg_visited_prop(n, d, steps, walker_class, walker_params=None, k=1):
        if not walker_params:
            walker = walker_class()
        else:
            walker = walker_class(walker_params)
        proportion_sum = np.zeros(steps+1)

        threshold = largest_comp(d) * 0.95
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_er_random_graph(n, d/n)
            results = Simulator.simulate_walk(graph, walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def plot_w_on_rg_visited_prop(n, d, steps, walker_class, walker_params=None, k=1, return_value=True):
        proportion_avg = Simulator.simulate_w_on_rg_visited_prop(
            n, d, steps, walker_class, walker_params, k)

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, p={:.2f}'.format(k, n, d/n))
        plt.title("Proportion of Visited Vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return proportion_avg

    @staticmethod
    def simulate_w_on_k_regular_visited_prop(n, d, steps, walker_class, walker_params=None, k=1):
        if not walker_params:
            walker = walker_class()
        else:
            walker = walker_class(walker_params)
        proportion_sum = np.zeros(steps+1)

        threshold = largest_comp(d) * 0.95
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_k_regular_random_graph(n, d)
            results = Simulator.simulate_walk(graph, walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def plot_w_on_k_regular_visited_prop(n, d, steps, walker_class, walker_params=None, k=1, return_value=True):
        proportion_avg = Simulator.simulate_w_on_k_regular_visited_prop(
            n, d, steps, walker_class, walker_params, k)

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, d={:d}'.format(k, n, d))
        plt.title("Proportion of Visited Vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return proportion_avg

    @staticmethod
    def simulate_w_on_dp_visited_prop(n, d_p, steps, walker_class, walker_params=None, k=1):
        if not walker_params:
            walker = walker_class()
        else:
            walker = walker_class(walker_params)
        proportion_sum = np.zeros(steps+1)

        d_avg = 0
        for d in d_p.keys():
            d_avg += d * d_p[d]

        threshold = largest_comp(d_avg) * 0.5
        valid_samples = 0
        d_seq = Graph.get_rg_degree_proportion_sequence_gen(n, d_p)
        while valid_samples < k:
            graph = Graph.get_rg_degree_distribution(d_seq)
            results = Simulator.simulate_walk(graph, walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def plot_w_on_dp_visited_prop(n, d_p, steps, walker_class, walker_params=None, k=1, return_value=True):
        proportion_avg = Simulator.simulate_w_on_dp_visited_prop(
            n, d_p, steps, walker_class, walker_params, k)

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, d_distribution={}'.format(k, n, d_p))
        plt.title("Proportion of Visited Vertices vs. # of Steps on BA model")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return proportion_avg

    @staticmethod
    def simulate_w_on_ba_visited_prop(n, m, steps, walker_class, walker_params=None, k=1):
        if not walker_params:
            walker = walker_class()
        else:
            walker = walker_class(walker_params)
        proportion_sum = np.zeros(steps+1)

        threshold = 0.95
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_BA_model_graph(n, m)
            results = Simulator.simulate_walk(graph, walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def plot_w_on_ba_visited_prop(n, m, steps, walker_class, walker_params=None, k=1, return_value=True):
        proportion_avg = Simulator.simulate_w_on_ba_visited_prop(
            n, m, steps, walker_class, walker_params, k)

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, m={:d}'.format(k, n, m))
        plt.title("Proportion of Visited Vertices vs. # of Steps on BA model")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return proportion_avg

    @staticmethod
    def simulate_w_on_ed_visited_prop(n, d_p, steps, walker_class, walker_params=None, k=1):
        if not walker_params:
            walker = walker_class()
        else:
            walker = walker_class(walker_params)
        proportion_sum = np.zeros(steps+1)

        d_avg = 0
        for d in d_p.keys():
            d_avg += d * d_p[d]

        threshold = largest_comp(d_avg) * 0.5
        valid_samples = 0
        while valid_samples < k:
            graph = Graph.get_expected_d_random_graph(n, d_p)
            results = Simulator.simulate_walk(graph, walker, steps)
            if results['proportions'][-1] >= threshold:
                proportion_sum += results['proportions']
                valid_samples += 1
        proportion_avg = proportion_sum / k
        return proportion_avg

    @staticmethod
    def plot_w_on_ed_visited_prop(n, d_p, steps, walker_class, walker_params=None, k=1, return_value=True):
        proportion_avg = Simulator.simulate_w_on_ed_visited_prop(
            n, d_p, steps, walker_class, walker_params, k)

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, d_distribution={}'.format(k, n, d_p))
        plt.title(
            "Proportion of Visited Vertices vs. # of Steps on expected degree graph")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()
        if return_value:
            return proportion_avg
