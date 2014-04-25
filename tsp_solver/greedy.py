from __future__ import print_function, division
################################################################################
# A simple algorithm for solving the Travelling Salesman Problem
# Finds a suboptimal solution
################################################################################
if "xrange" not in globals():
    #py3
    xrange = range
else:
    #py2
    def next(x): return x.next()
    

def optimize_solution( distances, connections ):
    """Tries to optimize solution, found by the greedy algorithm"""
    N = len(connections)
    path = restore_path( connections )
    def ds(i,j): #distance between ith and jth points of path
        return distances[path[i]][path[j]]
    d_total = 0.0
    optimizations = 0
    for a in xrange(N-1):
        b = a+1
        for c in xrange( b+2, N-1):
            d = c+1
            delta_d = ds(a,b)+ds(c,d) -( ds(a,c)+ds(b,d))
            if delta_d > 0:
                d_total += delta_d
                optimizations += 1
                connections[path[a]].remove(path[b])
                connections[path[a]].append(path[c])
                connections[path[b]].remove(path[a])
                connections[path[b]].append(path[d])

                connections[path[c]].remove(path[d])
                connections[path[c]].append(path[a])
                connections[path[d]].remove(path[c])
                connections[path[d]].append(path[b])
                path[:] = restore_path( connections )
    
    return optimizations, d_total
        
def restore_path( connections ):
    """Takes array of connections and returns a path.
    Connections is array of lists with 1 or 2 elements.
    These elements are indices of teh vertices, connected to this vertex
    Guarantees that first index < last index
    """
    #there are 2 nodes with valency 1 - start and end. Get them.
    start, end = [ idx for idx, conn in enumerate(connections)
                   if len(conn)==1 ]
    if start > end:
        start, end = end, start
    path = [start]
    prev_point = None
    cur_point = start
    while True:
        next_points = [pnt for pnt in connections[cur_point] 
                       if pnt != prev_point ]
        if not next_points: break
        next_point = next_points[0]
        path.append(next_point)
        prev_point, cur_point = cur_point, next_point
    return path

    
def solve_tsp( distances, optim_steps=3 ):
    """Given a distance matrix, finds a solution for the TSP problem.
    Returns list of vertex indices. 
    Guarantees that the first index is lower than the last"""
    N = len(distances)
    if N == 0: return []
    if N == 1: return [0]
    for row in distances:
        if len(row) != N: raise ValueError( "Matrix is not square")

    #State of the TSP solver algorithm.
    node_valency = [2] * N #Initially, each node has 2 sticky ends
    #for each node, stores 1 or 2 connected nodes
    connections = [[] for i in xrange(N)] 

    def join_segments():
        #segments of nodes. Initially, each segment contains only 1 node
        segments = [ [i] for i in xrange(N) ]
  
        def pairs_by_dist():
            print( "#### generating vertex pairs")
            pairs = [None] * (N*(N-1)//2)
            idx = 0
            for i in xrange(N):
                i_n = i*N    
                dist_i = distances[i]
                for j in xrange(i+1,N):
                    pairs[idx] = (dist_i[j],i_n + j) #for the economy of memory, store I and J packed.
                    idx += 1
            print( "#### sorting pairs by distance")
            pairs.sort()
            return pairs

        def nearest_pairs( sorted_pairs ):
            for d, i_j in sorted_pairs:
                i = i_j // N
                if not node_valency[i] : continue
                j = i_j % N
                if not node_valency[j] or (segments[i] is segments[j]): 
                    continue
                yield i, j

        pairs_gen = iter( nearest_pairs(pairs_by_dist()) )
        print( "#### joining segments")
        for itr in xrange(N-1):
            i,j = next(pairs_gen)
            node_valency[i] -= 1
            node_valency[j] -= 1
            connections[i].append(j)
            connections[j].append(i)
            #join the segments
            seg_i = segments[i]
            seg_j = segments[j]
            if len(seg_j) > len(seg_i):
                seg_i, seg_j = seg_j, seg_i
                i, j = j, i
            for node_idx in seg_j:
                segments[node_idx] = seg_i
            seg_i.extend(seg_j)
    
    join_segments()

    for passn in range(optim_steps):
        #print( "Optimization pass", passn)
        nopt, dtotal = optimize_solution( distances, connections )
        #print( "Done %d optimizations, total reduction %g"%(nopt, dtotal))
        if nopt == 0:
            break #Don't do useless optimization steps

    path = restore_path( connections )
    assert( len(path) == N )
    return path

def solve_tsp_numpy( distances, optim_steps=3 ):
    """Given a distance matrix, finds a solution for the TSP problem.
    Returns list of vertex indices.
    Version that uses Numpy - consumes less memory and works faster."""
    import numpy

    N = len(distances)
    if N == 0: return []
    if N == 1: return [0]
    for row in distances:
        if len(row) != N: raise ValueError( "Matrix is not square")

    #State of the TSP solver algorithm.
    node_valency = numpy.zeros( N, dtype = 'i1' )
    node_valency += 2 #Initially, each node has 2 sticky ends

    #for each node, stores 1 or 2 connected nodes
    connections = [[] for i in xrange(N)] 

    def join_segments():
        #segments of nodes. Initially, each segment contains only 1 node
        segments = [ [i] for i in xrange(N) ]
        def pairs_by_dist_np():
            print( "#### generating vertex pairs, numpy version")
            pairs = numpy.zeros( (N*(N-1)//2, ), dtype=('f4, i2, i2') )

            idx = 0
            for i in xrange(N):
                row_size = N-i-1
                dist_i = distances[i]
                pairs[idx:(idx+row_size)] = [ (dist_i[j], i, j)
                                              for j in xrange(i+1, N) ]
                idx += row_size
            print( "#### sorting pairs by distance")
            pairs.sort(order=["f1"]) #sort by the first field
            return pairs

        def nearest_pairs_np( sorted_pairs ):
            for d, i, j in sorted_pairs:
                if node_valency[i] and \
                   node_valency[j] and \
                   not (segments[i] is segments[j]): 
                    yield i, j

        pairs_gen = iter( nearest_pairs_np(pairs_by_dist_np()) )
        print( "#### joining segments")
        for itr in xrange(N-1):
            i,j = next(pairs_gen)
            node_valency[i] -= 1
            node_valency[j] -= 1
            connections[i].append(j)
            connections[j].append(i)
            #join the segments
            seg_i = segments[i]
            seg_j = segments[j]
            if len(seg_j) > len(seg_i):
                seg_i, seg_j = seg_j, seg_i
                i, j = j, i
            for node_idx in seg_j:
                segments[node_idx] = seg_i
            seg_i.extend(seg_j)
    
    join_segments()

    for passn in range(optim_steps):
        #print( "Optimization pass", passn)
        nopt, dtotal = optimize_solution( distances, connections )
        #print "Done %d optimizations, total reduction %g"%(nopt, dtotal)
        if nopt == 0:
            break #Don't do useless optimization steps

    path = restore_path( connections )
    assert( len(path) == N )
    return path

