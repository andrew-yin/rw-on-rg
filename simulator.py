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
        
        
@staticmethod
    def plot_rw_coverage_multisamples(n,p,steps,k):
        '''
        plot the average of each steps
        '''
        proportion_sum = np.array(np.zeros(steps+1))
        for j in range(k):
            graph = Graph.get_er_random_graph(n, p)           
            start = random.choice(list(graph.nodes))           
            random_walker = Walker(strategy="random", graph=graph, start=start)
            
            for i in range(steps):
                random_walker.move_dict()

            proportion_cur = [1]
            for i in range(steps):
                if random_walker.path[i+1] in random_walker.path[0:i+1]:
                    proportion_cur.append(proportion_cur[i])
                else:
                    proportion_cur.append(proportion_cur[i]+1)

            # proportion_cur = [len(set(random_walker.path[:i]))/n for i in range(1,len(random_walker.path)+1)]

            proportion_sum = proportion_sum + np.array(proportion_cur)/n

        proportion_avg = proportion_sum / n
        print(proportion_avg)
        plt.plot(np.arange(0, len(proportion_avg), step=1), proportion_avg)
        plt.title("Proportion of visited vertices vs. # of Steps")
        plt.xlabel("# of Steps")
        plt.ylabel("Proportion of visited vertices")
        plt.show()  
        

        
