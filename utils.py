from sympy.solvers import solve
from sympy import Symbol
from sympy import log


def largest_comp(d):
    """
    Returns the expected size (as a proportion of nodes) of the largest component in a random graph given expected degree d
    # TODO: Possibly numerically solve this
    """
    x = Symbol('x')
    equation = d*x + log(1-x)
    return round(float(solve(d*x + log(1-x), x)[1]), 5)
