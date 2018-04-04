import cv2 as cv
import numpy as np
import math

'''
CVTools 
designed to house any image processing functions. Consolidated the cv2 workhorse functions into "one liners"
'''
class CVTools:

    '''
    Apply Grayscale Filter
    ----------------------------------------------------------------------------------------------------------------------
    takes srcIm, applies a gaussian blur with kernel size of kSize and returns
    '''
    def toGray(self, srcIm):
        return dst


    '''
    Background Subtraction
    ----------------------------------------------------------------------------------------------------------------------
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
    ----------------------------------------------------------------------------------------------------------------------
    a dilation followed by an erosion at the specified kernel
    '''
    def Close(self, img, kSize):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (kSize, kSize))
        dst = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
        return dst

    '''
    Global Threshold
    ----------------------------------------------------------------------------------------------------------------------
    Apply gauss threshold 
    '''
    def Thresh(self, img, threshVal):
        ret, dst = cv.threshold(img, threshVal, 255, cv.THRESH_BINARY)
        return dst
    
    '''
    Gaussian Threshold
    ----------------------------------------------------------------------------------------------------------------------
    Apply gauss threshold 
    '''
    def GThresh(self, img):
        dst = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
        return dst

    '''
    Floodfill technique
    ----------------------------------------------------------------------------------------------------------------------
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
    Get Contours
    ----------------------------------------------------------------------------------------------------------------------
    For the processed image, return the list of contours found
    '''
    def GetContours(self, procimg):
        # finds all the contours, currently without using Canny edge detection. Uses RETR Tree hierarchy
        edge, contours, hierarchy = cv.findContours(procimg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours

    '''
    Get Non Mainbody Contours
    ----------------------------------------------------------------------------------------------------------------------
    Returns any contours that are not of the largest area
    '''
    def GetNonMainbodyContours(self, allContours, biggestContourIndex):

        nonMainbodyContourIndeces = []
        for i in range(len(allContours)):
            if (i != biggestContourIndex):
                nonMainbodyContourIndeces.append(i)

        return nonMainbodyContourIndeces


    '''
    Get Centroid
    ----------------------------------------------------------------------------------------------------------------------
    Given a set of contours. Go through each one and return the location of
    where the centroid should be. We will draw this centroid later. 
    Private
    '''

    def GetCentroid(self, c):
        # get center of contour using the moments
        # moments are specified by the string
        moments = cv.moments(c)

        if moments["m00"] != 0:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
        else:
            cX, cY = 0, 0

        return (cX, cY)

    '''
    Get Distance Between Two Points
    ----------------------------------------------------------------------------------------------------------------------
    Given two points (presumably centroids) get the euclidean distance between them
    '''

    def GetDistanceBetween(self, centroid1, centroid2):

        # get difference in x
        deltaX = centroid2[0] - centroid1[0]

        # get difference in y
        deltaY = centroid2[1] - centroid1[1]

        # use distance function on the differences
        distance = math.sqrt( math.pow(deltaX, 2) + math.pow(deltaY, 2) )

        return distance


    '''
    Get Largest Contour
    ----------------------------------------------------------------------------------------------------------------------
    Given a set of contours. Returns the contour with the largest area.
    '''
    def GetLargestContour(self, contours):
        largest = 0

        for i in range(len(contours)):
            # compare to the largest contour, and make sure that we don't accidentally grab the whole box!
            if (cv.contourArea(contours[i]) > cv.contourArea(contours[largest]) and cv.contourArea(contours[i]) < 4000000):
                largest = i

        # returns largest contours
        return largest


    '''
    Get Shape Factor
    ----------------------------------------------------------------------------------------------------------------------
    Given a contour, return shape factor
    '''
    def GetShapeFactor (self, c):
        # 4(pi)(Area)/(Perimeter)^2
        a = cv.contourArea(c)
        p = cv.arcLength(c, True)
        print (a)

        return (4 * (math.pi) * a / math.pow(p, 2) )



    ''' 
    Draw Centroid
    ----------------------------------------------------------------------------------------------------------------------
    given a dst image and contour c, draw a dot at the centroid
    ''' 
    def DrawCentroid(self, dst, c):

        # draw all the centroids as circles
        # c is the tuple which is the location of the centroid

        cv.circle(dst, c, 25, (0, 0, 255), -1)
        # cv.putText(dst, "center", (c[0] - 20, c[1] - 20), cv.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 10)


    ''' 
    Draw OffBody Centroid Connections
    ----------------------------------------------------------------------------------------------------------------------
    draw a line between two centroids
    ''' 
    def DrawOffBodyConnections(self, c1, c2, dst):
    
        # centroid c1 is the main body. Start Point
        # centroid c2 is the off body centroid. End Point
        lineColor = (255, 255, 255)
        thickness = 5
        cv.line(dst, c1, c2, lineColor, thickness)
    

    
    '''
    Visaulize Features
    ----------------------------------------------------------------------------------------------------------------------
    OpenCV Find contours method to trace the outline of the cell
    procimg: the processed image ready for contour searching
    dst: the image for the contours to be overlayed on

    Also draws the centroids and concentric circles that we use to collect data
    '''
    def VisualizeFeatures(self, procimg, dst):
        
        # get contour list
        contours = self.GetContours(procimg)

        # converts the main image from GRAY to RGB colorspace
        dst = cv.cvtColor(dst, cv.COLOR_GRAY2RGB)

        #------------------------------------

        #------------------------------------

            # theoretical next steps:
            # for each of these points, tell me if there is light in this or not.vertices
            #   now be careful, the background could definitely be light, where we probably would have to verify that there actually is something here
            # TODO need to make sure we aren't trying to get values for data that is out of bounds
            # TODO make sure that we aren't drawing (1) contour or (2) centroid or (3) circles until the analysis is finished. Otherwise data will obviously contain that crap
        #------------------------------------


        # draws the contours found from the processed image onto the original image to display
        cv.drawContours(dst, contours, -1, (128,255,0), 10)

        return dst






'''
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Unused Methods --------------------------------------------------------------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''


'''
Get Ellipse Vertices
-----------------------------------------------------------
Given a centroid, calculate points on an ellipse of a particular radii
Private
'''
def GetEllipseVertices(self, img, centroid, radius):
    # want to use ellipse2poly method
    # for a circle make sure the size parameter is (height, width) where h = w
    axes = (radius, radius) # the size of the first and second axes of the ellipse... h = w for a circle
    angleOfRot = 0          # angle of rotation: rotation off the central (vertical) axis of the ellipse
    startAngle = 0          # start angle of the points -> typically 0 
    endAngle = 360          # end angle of the points -> typically 360
    delta = 1               # the interpolation accuracy of the checks. We check every single angle for this

    # get the set of points
    vertices = cv.ellipse2Poly(centroid, axes, angleOfRot, startAngle, endAngle, delta) 

    return vertices



'''
Get And Draw Ellipse Data [UNDONE] No longer using this method....
-----------------------------------------------------------
Given a centroid, gets the ellipse data for a fixed number of rings with increasing radii.
At the points where data is taken, we draw a circle (although we should try just drawing dots)
'''
def GetAndDrawEllipseData(self, log, dst, origimg, centroid, startRadius, maxRadius, radiusStepSize):
    # draw one circle with constant radius around centroid

    # dst: image that circles will be drawn on top of
    # origimg: original image to grab light data from
    # startradius: first radius drawn
    # maxradius: maximum radius drawn
    # radiusStepSize: step size inbetween radii


    lineColor = (0, 0, 255)
    thickness = 5

    # get bounds of the image
    xBound = origimg.shape[0]   # rows
    yBound = origimg.shape[1]   # cols


    # i is the radius of the current circle being drawn
    for i in range (startRadius, maxRadius, radiusStepSize):
        
        # draw ellipse
        cv.circle(dst, centroid, i, lineColor, thickness)

        # collect ellipse data
        vertices = self.GetEllipseVertices(origimg, centroid, i)

        # for each datapoint in the circle we just identified , want to get the intensity of the color at that pixel point
        pixels = []
        isInBounds = True
        
        # for each point in the set of vertices, if in bounds of image, get the pixel intensity
        for j in range (len(vertices)):
            # if calculated vertex is out of bounds (x or y component)
            if (vertices[j][0] >= xBound or vertices[j][1] >= yBound):
                print("OUT OF BOUNDS!")
                isInBounds = False
                # stop iterating through this vertex set
                break
            else: 
                pixels.append(origimg[vertices[j][0], vertices[j][1]])
                # NOTE: two lines below get the pixel at position specified and prints to a log file
                # pixel = origimg[vertices[j][0], vertices[j][1]]
                # log.write("(" + str(vertices[j][0]) + ", " + str(vertices[j][1]) + "): " + str(pixel) + "\n")
        
        # TODO: have a boolean here that knows if we truncated the vertex set early. We wouldn't want this set
        # TODO: if a valid vertex set, add the data to the excel sheet
        

        # get the average value of pixels 
        # for j in range(len(pixels)):            










