import numpy as np
from graph import Graph
from walkers import RandomWalker
from matplotlib import pyplot as plt

class Collaboration():

    def __init__(self) -> None:
        pass
    
    def collab_rodos_rw_walk(graph, walker1, walker2, steps, calculate_prop = True):
        walker1.reset()
        walker2.reset()
        walker1.load_graph(graph)
        walker2.load_graph(graph)
        n = len(graph)

        walk1 = [walker1.cur]
        walk2 = [walker2.cur]
        proportions = np.ones(steps+1)
        proportions1 = np.ones(steps+1)
        proportions2 = np.ones(steps+1)

        visited = set(walk1 + walk2)
        visited1 = set(walk1)
        visited2 = set(walk2)

        for i in range(1, steps+1):
            walker1.move()
            walker2.move()
            walk1.append(walker1.cur)
            walk2.append(walker2.cur)
            if walker1.cur not in visited:
                visited.add(walker1.cur)
                if walker2.cur not in visited:
                    visited.add(walker2.cur)
                    proportions[i] = proportions[i-1] + 2
                else:
                    proportions[i] = proportions[i-1] + 1
    
            else:
                if walker2.cur not in visited:
                    visited.add(walker2.cur)
                    proportions[i] = proportions[i-1] + 1
                else:
                    proportions[i] = proportions[i-1]

            if walker1.cur not in visited1:
                visited1.add(walker1.cur)
                proportions1[i] = proportions1[i-1] + 1
            else:
                proportions1[i] = proportions1[i-1]

            if walker2.cur not in visited2:
                visited2.add(walker2.cur)
                proportions2[i] = proportions2[i-1] + 1
            else:
                proportions2[i] = proportions2[i-1]

        results = {
            'walk1': walk1,
            'walk2': walk2,
            }
        if calculate_prop:
            results['proportions1'] = proportions1/n
            results['proportions2'] = proportions2/n
            results['proportions'] = proportions/n
        return results


    def plot_rw_collab_on_erdos_rg_visited_largest_compo(n,p,steps, k = 1,  threshold = 0.5, return_proportion = True):
        walker1 = RandomWalker()
        walker2 = RandomWalker()

        proportion_sum =  np.zeros(steps+1)
        sample_count = 0
        while sample_count < k:
            graph = Graph.get_er_random_graph(n, p)
            results = Collaboration.collab_rodos_rw_walk(graph, walker1, walker2, steps)

            if results['proportions1'][-1] > threshold and results['proportions2'][-1] > threshold:
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

        if return_proportion:
            return proportion_avg

