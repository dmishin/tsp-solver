from PIL import Image
import numpy as np
from random import random as rand

def img2pointarray( N, arr):
    """convert array with values from 0 to 255 to a point cloud"""
    h,w = arr.shape
    rval = np.zeros( (2,N) )
    for i in xrange(N):
        while True:
            x = rand()*w
            y = rand()*h
            clr = rand()*255
            if arr[int(y),int(x)] < clr:
                break
        rval[:,i] = (x,h-y)
    return rval

def img_file2points(N, image_file):
    image = Image.open( image_file )
    return img2pointarray(N, np.asarray( image ))
    
