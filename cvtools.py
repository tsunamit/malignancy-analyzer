import cv2 as cv
import numpy as np

'''
CVTools 
designed to house any image processing functions. Consolidated the cv2 workhorse functions into "one liners"
'''
class CVTools:

    '''
    Apply Grayscale Filter
    -----------------------------------------------------------
    takes srcIm, applies a gaussian blur with kernel size of kSize and returns
    '''
    def toGray(self, srcIm):
        return dst


    '''
    Background Subtraction
    -----------------------------------------------------------
    takes srcIm, applies a gaussian blur with kernel size of kSize and returns
    '''
    def BackSub(self, srcIm, kSize):
        blurKernelSize = (kSize, kSize)
        # (image source; kernel size which is a tuple; and sigmaX which is the stdev)
        blur = cv.GaussianBlur(srcIm, blurKernelSize, 0)
        dst = cv.subtract(srcIm, blur)
        return dst

    '''
    Closing
    -----------------------------------------------------------
    a dilation followed by an erosion at the specified kernel
    '''
    def Close(self, img, kSize):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (kSize, kSize))
        dst = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
        return dst

    '''
    Global Threshold
    -----------------------------------------------------------
    Apply gauss threshold 
    '''
    def Thresh(self, img, threshVal):
        ret, dst = cv.threshold(img, threshVal, 255, cv.THRESH_BINARY)
        return dst
    
    '''
    Gaussian Threshold
    -----------------------------------------------------------
    Apply gauss threshold 
    '''
    def GThresh(self, img):
        dst = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
        return dst

    '''
    Floodfill technique
    -----------------------------------------------------------
    Fills in holes for a surrounded figure. 
    MUST PROVIDE PREVIOUSLY THRESHOLDED IMAGE!
    '''
    def ImFill (self, img):
        # copy thresholded image
        im_floodfill = img.copy()

        # handles mask used for floodfilling
        # Size somehow needs to be 2 pixels big/smaller? than image
        h, w = im_floodfill.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)

        # floodfilling from point 0,0
        cv.floodFill(im_floodfill, mask, (0,0), 255)

        # invert floodfilled image
        im_floodfillinv = cv.bitwise_not(im_floodfill)

        # combining images to get the foreground
        im_out = img | im_floodfillinv
        return im_out

    
    '''
    Get Trace
    -----------------------------------------------------------
    OpenCV Find contours method to trace the outline of the cell
    procimg: the processed image ready for contour searching
    dst: the image for the contours to be overlayed on
    '''
    def GetTrace(self, procimg, dst):
        # finds all the contours, currently without using Canny edge detection. Uses RETR Tree hierarchy
        edge, contours, hierarchy = cv.findContours(procimg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # converts the main image from GRAY to RGB colorspace
        dst = cv.cvtColor(dst, cv.COLOR_GRAY2RGB)

        #------------------------------------


        

        


        #------------------------------------
        # TESTING: draw the centroid

        for c in self.__GetCentroid(contours):

            # draw all the centroids as circles
            # c is the tuple which is the location of the centroid

            cv.circle(dst, c, 25, (0, 0, 255), -1)
            # cv.putText(dst, "center", (c[0] - 20, c[1] - 20), cv.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 10)

            self.__DrawCircles(c, dst)

        #------------------------------------


        # draws the contours found from the processed image onto the original image to display
        # HACK changed from draw all "-1" to "0" -> change back if need be
        cv.drawContours(dst, contours, -1, (128,255,0), 10)

        return dst

    '''
    Get Centroid
    -----------------------------------------------------------
    Given a set of contours. Go through each one and return the location of
    where the centroid should be. We will draw this centroid later. 
    Private
    '''
    def __GetCentroid(self, contours):

        centroids = []

        # loop through the given contours
        for c in contours:
            # get center of contours using the moments
            moments = cv.moments(c)

            if moments["m00"] != 0:
                cX = int(moments["m10"] / moments["m00"])
                cY = int(moments["m01"] / moments["m00"])
            else:
                cX, cY = 0, 0

            centroids.append((cX, cY))

        return centroids


    '''
    Draw Circles
    -----------------------------------------------------------
    Given a centroid, just draw a few circles with increasing radii. 
    Private
    '''
    def __DrawCircles(self, centroid, dst):
        # draw one circle with constant radius around centroid
        for i in range (75, 300, 25):
            cv.circle(dst, centroid, i, (0, 0, 255), 5)


    '''
    Get Largest Contour
    -----------------------------------------------------------
    Given a set of contours. Returns the contour with the largest area.
    '''















