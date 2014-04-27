import numpy
from tsp_solver.greedy import optimize_solution, restore_path, _join_segments, _restore_optimized_path

if "xrange" not in globals():
    #py3
    xrange = range
else:
    #py2
    def next(x): return x.next()

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
    return pairs

def nearest_pairs_np( N, node_valency, segments, sorted_pairs ):
    for d, i, j in sorted_pairs:
        if node_valency[i] and \
           node_valency[j] and \
           not (segments[i] is segments[j]): 
            yield i, j

def solve_tsp( distances, optim_steps=3 ):
    """Given a distance matrix, finds a solution for the TSP problem.
    Returns list of vertex indices.
    Version that uses Numpy - consumes less memory and works faster."""

    N = len(distances)
    if N == 0: return []
    if N == 1: return [0]
    for row in distances:
        if len(row) != N: raise ValueError( "Matrix is not square")

    #State of the TSP solver algorithm.
    node_valency = numpy.empty( N, dtype = 'i1' )
    node_valency.fill(2) #Initially, each node has 2 sticky ends

    #for each node, stores 1 or 2 connected nodes
    connections = [[] for i in xrange(N)] 

    def join_segments():
        #segments of nodes. Initially, each segment contains only 1 node
        segments = [ [i] for i in xrange(N) ]
        pairs_gen = nearest_pairs_np(N, node_valency, segments, pairs_by_dist_np(N, distances))
        _join_segments(N, pairs_gen, node_valency, connections, segments )
    join_segments()

    return _restore_optimized_path( distances, connections, optim_steps )
