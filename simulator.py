from graph import Graph
from walker import Walker
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
            'walk' : walk,
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
        random_walker = Walker(strategy="random")
        proportion_sum = np.zeros(steps+1)
        for i in range(k):
            graph = Graph.get_er_random_graph(n, p)           
            results = Simulator.simulate_walk(graph, random_walker, steps)

            proportion_sum += results['proportions']
        proportion_avg = proportion_sum / k

        plt.plot(np.arange(1, len(proportion_avg)+1, step=1), proportion_avg, label='k = {:d}'.format(k))
        plt.title("Proportion of Visited Vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.legend()
        plt.show()   
