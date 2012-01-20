from __future__ import with_statement
import pickle
import numpy as np
import math
from greedy_tsp import *
################################################################################
# Point cloud generators
################################################################################
def ring_points( N ):
    """Random set op points, located on the ring"""
    alpha = np.random.rand(N) * math.pi * 2
    r = np.random.normal(size=N)
    r *= 0.3
    r += 2

    return np.cos(alpha) * r, \
           np.sin(alpha) * r

def spot_points( N ):
    """Random points, forming a spot"""
    x = np.random.normal(size=N)    
    y = np.random.normal(size=N)
    return x,y

def box_points( N ):
    x = np.random.rand( N )
    y = np.random.rand( N )
    return x,y

def image_points( N, src_image ):
    from image2point_cloud import img_file2points
    try:
        p = img_file2points(N, src_image)
        return p[:,1],p[:,0]
    except IOError, err:
        print "Error reading file %s: %s"%(src_image, err)
        exit(2)
################################################################################
# Main application code
################################################################################
def make_dist_matrix(x, y):
    """Creates distance matrix for the given coordinate vectors"""
    N = len(x)
    xx = np.vstack( (x,)*N )
    yy = np.vstack( (y,)*N )
    return np.sqrt( (xx - xx.T)**2 + (yy - yy.T)**2 )

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser( description = "Travelling Salesman Problem demo solver. Searches for a suboptimal solution of a given N-point problem"  )
    parser.add_option( "-s", "--show-plot", 
                       action = "store_true", default=False,
                       dest="show_plot",
                       help="Plot generated solution using PyPlot" )
    parser.add_option( "-o", "--output", dest="output",
                       help="Ouptut file to store path to. By default, saves nothing"+
                          "Format is pickle of 2-tuple: (x,y), where x and y are Numpy arrays of point coordinates" )
    parser.add_option( "-p", "--pattern",
                       dest="pattern", default="spot",
                       help="Pattern to show. Available options are:\n"+
                       " spot    Symmetric spot of points, distributed by Gaussian law\n"+
                       " ring    Sircle of points\n"+
                       " box     1x1 box, uniformly filled with points\n"+
                       " image:/path/to/image   Uses BW image, filling black parts with points" )
    parser.add_option( "-n", "--num-points", type="int", default=500, dest="num_points",
                       help="Number of random points to generate" )

    (options, args) = parser.parse_args()

    N = options.num_points
    if N < 2:
        print "Need at least 2 points"
        exit(1)
    if N > 5000:
        print "Probably, number of points is too big. Try below 5000."

    IMAGE_PREFIX = "image:"
    if options.pattern == "spot":
        x,y = spot_points( N )
    elif options.pattern == "ring":
        x,y = ring_points( N )
    elif options.pattern == "box":
        x,y = box_points( N )
    elif options.pattern.startswith(IMAGE_PREFIX):
        x,y = image_points(N, options.pattern[len(IMAGE_PREFIX):])
    else:
        print "Unknown pattern:%s"%(options.pattern)
        exit(1)

    print "Solving sample TSP problem for %d points"%(N)
    path = solve_tsp_numpy( make_dist_matrix(x,y) )
    print "Solved"

    if options.output:
        try:
            with file( options.output, "w") as fl:
                pickle.dump( (x[path],y[path]), fl )
                print "Saved file %s"%(options.output)
        except IOError, err:
            print "IO exception:", err
            exit(2)

    if options.show_plot or not options.output:
        import matplotlib.pyplot as pp
        pp.plot( x[path], -y[path], 'k-' )
        pp.show()
