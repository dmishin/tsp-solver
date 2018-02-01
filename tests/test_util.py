from unittest import TestCase
from tsp_solver import util

if "xrange" in globals():
    #py2
    range = xrange
    def next(x): return x.next()
    

class TestGreedy( TestCase ):
    def test_path_cost(self):
        D = [[],
             [1],
             [2, 3]]

        #0-1 : 1
        #0-2 : 2
        #1-2 : 3
        
        #special cases:
        self.assertEqual(util.path_cost(D, []), 0)
        self.assertEqual(util.path_cost(D, [0]), 0)
        self.assertEqual(util.path_cost(D, [1]), 0)
        self.assertEqual(util.path_cost(D, [2]), 0)

        #general case:
        self.assertEqual(util.path_cost(D, [0,1]), 1)
        self.assertEqual(util.path_cost(D, [1,0]), 1)
        
        self.assertEqual(util.path_cost(D, [0,1,2]), 1 + 3)
        self.assertEqual(util.path_cost(D, [2,1,0]), 3 + 1)
        self.assertEqual(util.path_cost(D, [2,0,1]), 2 + 1)

        self.assertEqual(util.path_cost(D, [2,0,1,2,1]), 2 + 1 + 3 + 3)
        
