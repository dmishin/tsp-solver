from __future__ import print_function
from tsp_solver import greedy
from random import random, seed
from time import time

def run_test( name, solve_tsp, npoints=100, optim_steps=3, seed_value = 1000 ):
    D = [[0 for i in range(npoints)]
         for j in range(npoints)]
    seed( seed_value )
    for i in range(npoints):
        for j in range(i+1, npoints):
            d = random()
            D[i][j] = d
            D[j][i] = d

    start = time()

    path = solve_tsp( D, optim_steps = optim_steps )

    elapsed = time() - start

    print( "Method:", name )
    print( "Optimization steps:", optim_steps )
    print( "N points:", npoints )
    print( "Time elapsed:", elapsed, "s" )




if __name__=="__main__":
    print("=============================")
    run_test("Greedy TSP, pure python", greedy.solve_tsp, npoints = 500)
    print("=============================")
    try:
        from tsp_solver import greedy_numpy
        run_test("Greedy TSP, numpy", greedy_numpy.solve_tsp, npoints = 500)
    except ImportError as err:
        print ("No numpy module")
