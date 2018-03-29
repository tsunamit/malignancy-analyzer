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

f = open("log.txt", "w+")

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
# TODO fix image 8. seems to not work well with this
img_main = cv.imread('img/2.tif')
img_main = cv.cvtColor(img_main, cv.COLOR_RGB2GRAY)
orig = img_main.copy()
# original image to draw on
origDraw = img_main.copy()

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



'''
//////////////////////////////////////
// Data Collection and Drawing
//////////////////////////////////////
'''

# Data to collect
'''
* contour data ? this already gets collected though
* light data at the specified points... make sure you handle background at some point
'''

# get contours, largest contour index, and the largest contour centroid
imgContours = cvt.GetContours(dst3)
largestContourIndex = cvt.GetLargestContour(imgContours)
largestContourCentroid = cvt.GetCentroid(imgContours[largestContourIndex])

# get all other centroids, store in an array offBodyCentroids
offBodyContourIndeces = cvt.GetNonMainbodyContours(imgContours, largestContourIndex)
offBodyCentroids = []
for i in range(len(offBodyContourIndeces)):
    c = cvt.GetCentroid(imgContours[offBodyContourIndeces[i]])
    offBodyCentroids.append(c)

# get the distance between the offbodies and the central centroid. Store in an array
distancesFromCentroid = []

for i in range(len(offBodyCentroids)):
    print ("offpoint: " + str(offBodyCentroids[i]))
    print("central point: " + str(largestContourCentroid))
    d = cvt.GetDistanceBetween(largestContourCentroid, offBodyCentroids[i])
    print(d)

    # add to array
    distancesFromCentroid.append(d)

# HACK get average dist from centroid
# HACK get max dist from centroid






# Data to draw
'''
* trace cell contours
* draw centroids
'''

# trace the cell contours
# NOTE: dst3 is the last processed image
trace = cvt.VisualizeFeatures(dst3, origDraw)



'''
//////////////////////////////////////
// Displaying Images
//////////////////////////////////////
'''
# display images
toDisplay = [orig, dst, dst1, dst2, dst3, trace]
# TODO turn the other images into BGR so they don't look terrible\
d.small_grid(toDisplay)
# d.SingleView ("img", trace)


'''
TODO:
* Would like to have a slider to drag to adjust blur and see the effect across all the images

* click on matplot img to open up a cv imshow?
'''