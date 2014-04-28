from __future__ import print_function, division
from unittest import TestCase
from tsp_solver import greedy, greedy_numpy

if "xrange" not in globals():
    #py3
    xrange = range
else:
    #py2
    def next(x): return x.next()
    

def make_dist_matrix( n, default, ijd_tuples ):
    """Utility function to make square distance matrices"""
    dist = [ [default for j in xrange(n)]
             for i in xrange(n)]
    for i,j,d in ijd_tuples:
        dist[i][j] = d
        dist[j][i] = d
    return dist

def make_test_case( solver ):
    """Reuse the same test case for 2 different solver functions"""
    class TestGreedy( TestCase ):
        def test_empty_graph(self):
            distances = []
            vertices = solver( distances )
            self.assertListEqual( vertices, [] )

        def test_single_vertes(self):
            vs = solver( [[1]] )
            self.assertListEqual( vs, [0] )

        def test_two_vertices(self):
            dist = [[0, 1],
                    [1, 0]]
            vs = solver( dist )
            self.assertListEqual( vs, [0,1] )

        def test_three_vertices(self):
            #Make a simple matrix with 2 short paths: 0->2 and 2->1
            D = make_dist_matrix(3, 1000, [(0,2,5), (2,1,1)])
            vs = solver( D )
            self.assertListEqual( vs, [0,2,1] )

    return TestGreedy

class TestGreedySimple( make_test_case( greedy.solve_tsp ) ):
    pass

class TestGreedyNumpy( make_test_case( greedy_numpy.solve_tsp ) ):
    pass


class TestPairsByDist( TestCase ):
    def test_pairs_by_dist(self):
        dist = [[0,2,3],
                [2,0,5],
                [3,5,0]]
        N = 3
        pbd = list( greedy.pairs_by_dist( N, dist ) )
        #Returns indices of node pairs, sorted by distance
        expected = [ (0,1),
                     (0,2),
                     (1,2) ]
        self.assertListEqual( pbd, expected )
        
    def test_pairs_by_dist_numpy(self):
        dist = [[0,2,3],
                [2,0,5],
                [3,5,0]]
        N = 3
        pbd = list( greedy_numpy.pairs_by_dist_np( N, dist ) )

        expected = [ (0,1),
                     (0,2),
                     (1,2) ]
        self.assertEqual( len(expected), len( pbd ) ) #lists must have same lenght
        for idx, i_j in enumerate(expected):
            i1, j1 = pbd[idx]
            self.assertEqual( i_j, (i1,j1), "List item %d must be the same"%(idx) )
        
