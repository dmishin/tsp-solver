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
    """Utility function to make triangular distance matrices"""
    dist = [ [default for j in xrange(i)]
             for i in xrange(n)]
    for i,j,d in ijd_tuples:
        if i<j :
            i,j = j,i
        dist[i][j] = d
    return dist

def make_test_case( solver ):
    """Reuse the same test case for 2 different solver functions"""
    class TestGreedy( TestCase ):
        def test_empty_graph(self):
            distances = []
            vertices = solver( distances )
            self.assertListEqual( vertices, [] )

        def test_single_vertex(self):
            vs = solver( [[1]] )
            self.assertListEqual( vs, [0] )

        def test_two_vertices(self):
            dist = [[0, 1],
                    [1, 0]]
            vs = solver( dist )
            self.assertListEqual( vs, [0,1] )
            
        def test_two_vertices_endpoints(self):
            dist = [[0, 1],
                    [1, 0]]
            vs = solver( dist, endpoints=(0,1) )
            self.assertListEqual( vs, [0,1] )
            
            vs = solver( dist, endpoints=(1,0) )
            self.assertListEqual( vs, [1,0] )

        def test_three_vertices(self):
            #Make a simple matrix with 2 short paths: 0->2 and 2->1
            D = make_dist_matrix(3, 1000, [(0,2,5), (2,1,1)])
            vs = solver( D )
            self.assertListEqual( vs, [0,2,1] )

        def test_long_path( self ):
            D = make_dist_matrix(10, 1000, 
                                 [( 0,2,1),
                                  ( 2,4,1),
                                  ( 4,6,1),
                                  ( 6,8,1),
                                  ( 8,9,1),
                                  ( 9,7,1),
                                  ( 7,5,1),
                                  ( 5,3,1),
                                  ( 3,1,1) ])
            vs = solver(D)
            self.assertListEqual( vs, [0,2,4,6,8,9,7,5,3,1] )
                           
        def test_endpoints( self ):
            """Check that endpoints are processed correctly"""
            D = make_dist_matrix(3, 1000, [(0,2,5), (2,1,1)])
            
            for start in (0,1,2):
                for end in (0,1,2):
                    if start == end:continue
                    vs = solver( D, endpoints=(start, end) )

                    details = "endpoints={}, D={}, result={}".format((start, end), repr(D), repr(vs))
                    self.assertEqual(len(vs), 3, "Must return 3 nodes when "+details)
                    self.assertEqual(vs[0], start, "Must start correctly "+details)
                    self.assertEqual(vs[2], end, "Must end correctly "+details)

                    
            
    return TestGreedy

class TestGreedySimple( make_test_case( greedy.solve_tsp ) ):
    pass

class TestGreedyNumpy( make_test_case( greedy_numpy.solve_tsp ) ):
    pass


class TestPairsByDist( TestCase ):
    def test_pairs_by_dist(self):
        dist = [[],
                [2],
                [3,5]]
        N = 3
        pbd = list( greedy.pairs_by_dist( N, dist ) )
        #Returns indices of node pairs, sorted by distance
        expected = [ (1,0),
                     (2,0),
                     (2,1) ]
        self.assertListEqual( pbd, expected )
        
    def test_pairs_by_dist_numpy(self):
        dist = [[],
                [2],
                [3,5]]
        N = 3
        pbd = list( greedy_numpy.pairs_by_dist_np( N, dist ) )

        expected = [ (1,0),
                     (2,0),
                     (2,1) ]
        self.assertEqual( len(expected), len( pbd ) ) #lists must have same lenght
        for idx, i_j in enumerate(expected):
            i1, j1 = pbd[idx]
            self.assertEqual( i_j, (i1,j1), "List item %d must be the same"%(idx) )
        
