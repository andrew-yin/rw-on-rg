import walkers
from graph import Graph
# from walkers.walker import Walker
from walkers.random_walker import RandomWalker
import random
import numpy as np
import matplotlib.pyplot as plt


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

        # plt.plot(np.arange(1, len(proportion_avg)+1, step=1), proportion_avg, label='k = {:d}'.format(k))
        # plt.title("Proportion of Visited Vertices vs. # of Steps")
        # plt.xlabel("# of Steps")
        # plt.ylabel("Proportion of visited vertices")
        # plt.legend()
        # plt.show()
        return proportion_avg

    @staticmethod
    def plot_rw_on_k_regular_visited_prop(d, n, steps, k=1):
        """
        Plot the average proportion of visited vertices at each step
        of a random walk on a k-regular random graph over k samples
        """
        random_walker = RandomWalker()
        proportion_sum = np.zeros(steps+1)
        for i in range(k):
            graph = Graph.get_k_regular_random_graph(d, n)
            results = Simulator.simulate_walk(graph, random_walker, steps)

            proportion_sum += results['proportions']
        proportion_avg = proportion_sum / k

        # plt.plot(np.arange(1, len(proportion_avg)+1, step=1), proportion_avg, label='k = {:d}'.format(k))
        # plt.text(25, 0.9, 'n={:n}'.format(n), horizontalalignment='center')
        # plt.title("k-regular: Proportion of Visited Vertices vs. # of Steps")
        # plt.xlabel("# of Steps")
        # plt.ylabel("Proportion of visited vertices")
        # plt.legend()
        # plt.show()
        return proportion_avg


if __name__ == '__main__':
    n, steps, k = 100, 1000, 1000
    d = 10
    p = 10/n
    plt.plot()
    a = Simulator.plot_rw_on_rg_visited_prop(n, p, steps, k)
    t = np.arange(1, len(a)+1, step=1)
    b = Simulator.plot_rw_on_k_regular_visited_prop(d, n, steps, k)
    plt.plot(t, a, label='Erdos-Renyi')
    plt.plot(t, b, label='k-Regular')
    plt.title("ER vs. k-Regular: Proportion of Visited Vertices vs. # of Steps")
    plt.xlabel("# of Steps")
    plt.ylabel("Proportion of visited vertices")
    plt.legend(title='n={:n}, '.format(n)+'k={:d}'.format(k))
    plt.show()
