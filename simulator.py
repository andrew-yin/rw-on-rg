from graph import Graph
from walker import Walker
import random
import numpy as np
import matplotlib.pyplot as plt

class Simulator:

    def __init__(self):
        pass

    @staticmethod
    def plot_rw_visited_prop(n, p, steps):
        graph = Graph.get_er_random_graph(n, p)
        start = random.choice(list(graph.nodes))
        random_walker = Walker(strategy="random", graph=graph, start=start)

        walk = [start]
        for i in range(steps):
            random_walker.move()
            walk.append(random_walker.get_current_node())

        proportion = []
        for i in range(1, len(walk)+1):
            proportion.append(len(set(walk[:i]))/n)

        plt.plot(np.arange(0, len(proportion), step=1), proportion)
        plt.title("Proportion of visited vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.show()

        
        print('hi')
