#############################################
##       COLLABORATION UTIL FUNCTIONS      ##
#############################################

import walkers
import numpy as np

def simulate_rw_collab_vs_single(graph, collab_num, k, collab_steps_per_iter):
    single_rw = walkers.RandomWalker()
    collab_rws = [walkers.RandomWalker() for _ in range(collab_num)]

    single_covered_avg = np.zeros(collab_num*collab_steps_per_iter+1)
    collab_covered_avg = np.zeros(collab_steps_per_iter+1)
    for _ in range(k):
        single_rw.reset()
        for i in range(collab_num):
            collab_rws[i].reset()
    
        single_rw.load_graph(graph)
        for i in range(collab_num):
            collab_rws[i].load_graph(graph)
    
        single_covered = np.zeros(collab_num*collab_steps_per_iter+1)
        collab_covered = np.zeros(collab_steps_per_iter+1)

        single_visited = set([single_rw.cur])
        collab_visited = set([collab_rws[i].cur for i in range(collab_num)])
    
        single_covered[0] = len(single_visited)
        collab_covered[0] = len(collab_visited)

        for i in range(1, collab_steps_per_iter+1):
            single_covered[i] = single_covered[i-1]
            single_rw.move()
            if single_rw.cur not in single_visited:
                single_visited.add(single_rw.cur)
                single_covered[i] += 1
            
            collab_covered[i] = collab_covered[i-1]
            for j in range(collab_num):
                collab_rws[j].move()
                if collab_rws[j].cur not in collab_visited:
                    collab_visited.add(collab_rws[j].cur)
                    collab_covered[i] += 1
        collab_covered_avg += collab_covered
        
        for i in range(collab_steps_per_iter+1, collab_num*collab_steps_per_iter+1):
            single_covered[i] = single_covered[i-1]
            single_rw.move()
            if single_rw.cur not in single_visited:
                single_visited.add(single_rw.cur)
                single_covered[i] += 1
        single_covered_avg += single_covered
    
    collab_covered_avg /= k
    single_covered_avg /= k

    return collab_covered_avg, single_covered_avg

def simulate_rw_star_collab_vs_single(graph, collab_num, k, collab_steps_per_iter):
    single_rw = walkers.RandomWalker()
    collab_rws = [walkers.RandomWalker() for _ in range(collab_num)]

    single_covered_avg = np.zeros(collab_num*collab_steps_per_iter+1)
    collab_covered_avg = np.zeros(collab_steps_per_iter+1)
    for _ in range(k):
        single_rw.reset()
        for i in range(collab_num):
            collab_rws[i].reset()
    
        single_rw.load_graph(graph)
        for i in range(collab_num):
            collab_rws[i].load_graph(graph)
        for i in range(1, collab_num):
            collab_rws[i].cur = collab_rws[0].cur
    
        single_covered = np.zeros(collab_num*collab_steps_per_iter+1)
        collab_covered = np.zeros(collab_steps_per_iter+1)

        single_visited = set([single_rw.cur])
        collab_visited = set([collab_rws[i].cur for i in range(collab_num)])
    
        single_covered[0] = len(single_visited)
        collab_covered[0] = len(collab_visited)

        for i in range(1, collab_steps_per_iter+1):
            single_covered[i] = single_covered[i-1]
            single_rw.move()
            if single_rw.cur not in single_visited:
                single_visited.add(single_rw.cur)
                single_covered[i] += 1
            
            collab_covered[i] = collab_covered[i-1]
            for j in range(collab_num):
                collab_rws[j].move()
                if collab_rws[j].cur not in collab_visited:
                    collab_visited.add(collab_rws[j].cur)
                    collab_covered[i] += 1
        collab_covered_avg += collab_covered
        
        for i in range(collab_steps_per_iter+1, collab_num*collab_steps_per_iter+1):
            single_covered[i] = single_covered[i-1]
            single_rw.move()
            if single_rw.cur not in single_visited:
                single_visited.add(single_rw.cur)
                single_covered[i] += 1
        single_covered_avg += single_covered
    
    collab_covered_avg /= k
    single_covered_avg /= k

    return collab_covered_avg, single_covered_avg