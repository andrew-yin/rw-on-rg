import numpy as np
import matplotlib.pyplot as plt

from graph import Graph
from walkers import RandomWalker


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
    def plot_rw_on_rg_visited_prop(n, p, steps, k=1):
        """
        Plot the average proportion of visited vertices at each step 
        of a random walk on a random graph over k samples
        """
        random_walker = RandomWalker()
        proportion_sum = np.zeros(steps+1)
        for i in range(k):
            graph = Graph.get_er_random_graph(n, p)
            results = Simulator.simulate_walk(graph, random_walker, steps)
            proportion_sum += results['proportions']
        proportion_avg = proportion_sum / k

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, p={:.2f}'.format(k, n, p))
        plt.title("Proportion of Visited Vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_rw_on_rg_visited_prop_largest_compo(n, p ,steps, k =1, threshold = 0.5, return_avg = True):
        """
        Plot the average proportion of visited vertices at each step 
        of a random walk on a random graph over k samples
        exclude the sample with less than 0.5
        """
        random_walker = RandomWalker()
        proportion_sum = np.zeros(steps+1)
        sample_count = 0
        while sample_count < k:
            graph = Graph.get_er_random_graph(n, p)
            results = Simulator.simulate_walk(graph, random_walker, steps)

            if results['proportions'][-1] > threshold:
                proportion_sum += results['proportions']
                sample_count += 1 
            else:
                continue

        proportion_avg = proportion_sum / k

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1),
                 proportion_avg, label='k = {:d}, n={:d}, p={:.2f}'.format(k, n, p))
        plt.title("Proportion of Visited Vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()

        if return_avg:
            return proportion_avg
