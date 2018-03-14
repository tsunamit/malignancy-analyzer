import cv2 as cv
import numpy as np
import datetime
from display import Display
from cvtools import CVTools

'''
//////////////////////////////////////
// SPLASH SCREEN
//////////////////////////////////////
'''

print("CREATOR: tsunamit\n" + "OPENCV " + cv.__version__)
print('RUNTIME: ' + (str)(datetime.datetime.now()))
print("/\n/\n/\nRUNNING\n/\n/\n/\n")

'''
//////////////////////////////////////
// Variables
//////////////////////////////////////
'''
# instantiate needed vars
cvt = CVTools()
d = Display()

# HACK USER CHANGED VARS
# backgroundSubK must be odd
backgroundSubK = 255
closeK = 25
threshVal = 25

# load images to vars here. 0 is the gray mask
# test (invasive cell), 6 (complicated), 3 (perfect)
# 10.tif is the confocal
img_main = cv.imread('img/3.tif')
img_main = cv.cvtColor(img_main, cv.COLOR_RGB2GRAY)
orig = img_main.copy()

'''
//////////////////////////////////////
// Image Processing 
//////////////////////////////////////
'''
# blur image
dst = cvt.BackSub(img_main, backgroundSubK)

# close image
dst1 = cvt.Close(dst, closeK)

# global threshold
dst2 = cvt.Thresh(dst1, threshVal)

# test close
dst2 = cvt.Close(dst2, 50)

# floodfill
dst3 = cvt.ImFill(dst2)

# trace the cell contours
trace = cvt.GetTrace(dst3, img_main)


'''
//////////////////////////////////////
// Displaying Images
//////////////////////////////////////
'''
# display images
toDisplay = [orig, dst, dst1, dst2, dst3, trace]
# TODO turn the other images into BGR so they don't look terrible
# HACK uncomment this line below!!!!!! 
# d.small_grid(toDisplay)

d.SingleView ("img", trace)


'''
TODO:
* Would like to have a slider to drag to adjust blur and see the effect across all the images

* click on matplot img to open up a cv imshow?
'''