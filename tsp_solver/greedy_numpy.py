import numpy
from tsp_solver.greedy import solve_tsp as base_solve_tsp

if "xrange" not in globals():
    #py3
    xrange = range
else:
    #py2
    pass

def pairs_by_dist_np(N, distances):
    pairs = numpy.zeros( (N*(N-1)//2, ), dtype=('f4, i2, i2') )

    idx = 0
    for i in xrange(N):
        row_size = N-i-1
        dist_i = distances[i]
        pairs[idx:(idx+row_size)] = [ (dist_i[j], i, j)
                                      for j in xrange(i+1, N) ]
        idx += row_size
    pairs.sort(order=["f0"]) #sort by the first field
    return pairs[["f1","f2"]]


def solve_tsp( distances, optim_steps=3,pairs_by_dist = pairs_by_dist_np ):
    """Given a distance matrix, finds a solution for the TSP problem.
    Returns list of vertex indices.
    Version that uses Numpy - consumes less memory and works faster."""
    return base_solve_tsp( distances, optim_steps=optim_steps, pairs_by_dist=pairs_by_dist_np )
