from simulator import Simulator

def main():
    n = 2000
    p = 6/n
    steps = 10000
    Simulator.generate_rw_visited_prop(n, p, steps)

if __name__ == "__main__":
    main()