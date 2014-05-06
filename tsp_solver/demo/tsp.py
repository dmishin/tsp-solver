from __future__ import with_statement, print_function
import pickle
import numpy as np
import math
#from tsp_solver.greedy import solve_tsp
from tsp_solver.greedy_numpy import solve_tsp

try:
    import psyco
    psyco.full()
except:
    pass


################################################################################
# Point cloud generators
################################################################################
def ring_points( N ):
    """Random set op points, located on the ring"""
    alpha = np.random.rand(N) * math.pi * 2
    r = np.random.normal(size=N)
    r *= 0.3
    r += 2

    points = np.vstack( (np.cos(alpha), np.sin(alpha)) )
    points *= r
    return points

def spot_points( N ):
    """Random points, forming a spot"""
    xy = np.random.normal(size=(2,N))
    return xy

def box_points( N ):
    xy = np.random.rand( (2,N) )
    return xy

def image_points( N, src_image ):
    from image2point_cloud import img_file2points
    try:
        p = img_file2points(N, src_image)
        return p
    except IOError as err:
        print( "Error reading file %s: %s"%(src_image, err))
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

def main():
    from optparse import OptionParser

    parser = OptionParser( description = "Travelling Salesman Problem demo solver. Searches for a suboptimal solution of a given N-point problem"  )
    parser.add_option( "-s", "--show-plot", 
                       action = "store_true", default=False,
                       dest="show_plot",
                       help="Plot generated solution using PyPlot" )
    parser.add_option( "-o", "--output", dest="output",
                       help="Ouptut file to store path to. By default, saves nothing. "+
                          "Data is in the Numpy format, single 2xN array of point coordinates" )
    parser.add_option( "-p", "--pattern",
                       dest="pattern", default="spot",
                       help="Pattern to show, one of [spot, ring, box, image:path]. The 'spot' generates round spot of points, distributed by Gaussian law. "+
                       "The 'ring' produces a ring of points. "+
                       "The 'box' produces uniformly filled rectangle. "+
                       "The image:/path/to/image uses BW image, where black areas are filled with points" )
    parser.add_option( "-n", "--num-points", type="int", default=500, dest="num_points",
                       help="Number of random points to generate, less than 5000 (actually, 3000 is a practical limit)" )

    (options, args) = parser.parse_args()

    N = options.num_points
    if N < 2:
        parser.error ("Need at least 2 points")
    if N > 5000:
        print ("Warning: probably, number of points is too big. Try below 5000.")

    IMAGE_PREFIX = "image:"
    if options.pattern == "spot":
        xy = spot_points( N )
    elif options.pattern == "ring":
        xy = ring_points( N )
    elif options.pattern == "box":
        xy = box_points( N )
    elif options.pattern.startswith(IMAGE_PREFIX):
        xy = image_points(N, options.pattern[len(IMAGE_PREFIX):])
    else:
        print ("Unknown pattern:%s"%(options.pattern))
        exit(1)

    print ("Solving sample TSP problem for %d points"%(N))
    path = solve_tsp( make_dist_matrix(xy[0,:],xy[1,:]) )
    print ("Solved")

    if options.output:
        try:
            with file( options.output, "w") as fl:
                np.save( fl, xy[:,path])
                print ("Saved file %s"%(options.output))
        except IOError as err:
            print ("IO exception:", err)
            exit(2)

    if options.show_plot or not options.output:
        try:
            import matplotlib.pyplot as pp
        except ImportError as err:
            print ("Can't show plot, matplotlib module not available:", err)
            print ("Either install matplotlib or set an -o option" )
            exit(2)

        pp.plot( xy[0,path], xy[1,path], 'k-' )
        pp.show()

if __name__ == '__main__':
    main()
