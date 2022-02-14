def largest_comp(d):
    """
    Returns the expected size (as a proportion of nodes) of the largest component in a random graph given expected degree d
    # TODO: Possibly numerically solve this
    """
    if d == 2:
        f_d = 0.797
    elif d == 3:
        f_d = 0.94
    elif d == 4:
        f_d = 0.98
    elif d == 5:
        f_d = 0.993
    elif d == 10:
        f_d = 0.999
    return f_d
