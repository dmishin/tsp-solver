from __future__ import print_function, division
from unittest import TestCase
from tsp_solver import greedy, greedy_numpy
import random
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
            
        def test_single_vertex_loop(self):
            vs = solver( [[1]], endpoints=(0,0) )
            self.assertListEqual( vs, [0,0] )

        def test_two_vertices(self):
            dist = [[0, 1],
                    [1, 0]]
            vs = solver( dist )
            self.assertListEqual( vs, [0,1] )
            
        def test_two_vertices_loop(self):
            dist = [[0, 1],
                    [1, 0]]
            vs = solver( dist, endpoints=(0,0) )
            self.assertListEqual( vs, [0,1,0] )
            
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
            
        def test_long_loop( self ):
            D = make_dist_matrix(10, 1000, 
                                 [( 0,2,1),
                                  ( 2,4,1),
                                  ( 4,6,1),
                                  ( 6,8,1),
                                  ( 8,9,1),
                                  ( 9,7,1),
                                  ( 7,5,1),
                                  ( 5,3,1),
                                  ( 3,1,1),
                                  ( 1,0,1)])
            vs = solver(D, endpoints=(0,0))
            #solution muse be on of 02468975310 or the reverse
            if vs[1] == 2:
                self.assertListEqual( vs, [0,2,4,6,8,9,7,5,3,1,0] )
            elif vs[1] == 1:
                self.assertListEqual( vs, [0,2,4,6,8,9,7,5,3,1,0][::-1] )
            else:
                raise ValueError("Neither of two solutions obtained!")
                           
        def test_endpoints( self ):
            """Check that endpoints are processed correctly"""
            D = make_dist_matrix(3, 1000, [(0,2,5), (2,1,1)])

            #None means unspecified enpoint
            for start in (0,1,2, None):
                for end in (0,1,2, None):
                    vs = solver( D, endpoints=(start, end) )
                    is_loop = (start is not None) and (start==end)
                    expect_len = 4 if is_loop else 3                    
                    details = "endpoints={}, D={}, result={}".format((start, end), repr(D), repr(vs))
                    self.assertEqual(len(vs), expect_len, "Must return {} nodes when ".format(expect_len)+details)

                    if start is not None:
                        self.assertEqual(vs[0], start, "Must start correctly "+details)
                    if end is not None:
                        self.assertEqual(vs[-1], end, "Must end correctly "+details)


        def test_endpoints_large( self ):
            """Check that endpoints are processed correctly"""
            N = 10
            #Make a deterministic random matrix
            for seed in range(10):
                random.seed(31415+seed)
                D = [[random.randint(0,1000) for j in range(m)]
                     for m in range(N)]

                #None means unspecified enpoint
                for start in list(range(N))+[None]:
                    for end in list(range(N))+[None]:
                        vs = solver( D, endpoints=(start, end) )
                        
                        is_loop = (start is not None) and (start==end)
                        expect_len = N+1 if is_loop else N

                        details = "seed={}, endpoints={}, D={}, result={}".format(seed, (start, end), repr(D), repr(vs))
                        self.assertEqual(len(vs), expect_len, "Must return {} nodes when ".format(expect_len)+details)

                        if start is not None:
                            self.assertEqual(vs[0], start, "Must start correctly "+details)
                        if end is not None:
                            self.assertEqual(vs[-1], end, "Must end correctly "+details)

                        
                        
            
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
        
