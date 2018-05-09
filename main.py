import cv2 as cv
import numpy as np
import datetime
import os                       # for path operations
import output_handler
from display import Display
from cvtools import CVTools

def run():

    '''
    ////////////////////////////////////////////////////////////////////////////
    // SPLASH SCREEN - DATA PREP
    ////////////////////////////////////////////////////////////////////////////
    '''

    print("CREATOR: tsunamit\n" + "OPENCV " + cv.__version__)
    print('RUNTIME: ' + (str)(datetime.datetime.now()))
    print("/\n/\n/\nRUNNING\n/\n/\n/\n")

    f = open("log.txt", "w+")
    # HACK make new log files each run!!!!
    m_csvFile = open("data.csv", "w+")

    '''
    ////////////////////////////////////////////////////////////////////////////
    // SELECT IMAGE DIRECTORY
    ////////////////////////////////////////////////////////////////////////////
    '''

    # want to specitfy a path here
    imgFileNames = []
    for subdir, dirs, files in os.walk('./img/'):
        for fileName in files:
            imgFileNames.append(fileName)
            print (fileName)


    '''
    ////////////////////////////////////////////////////////////////////////////
    // Variables
    ////////////////////////////////////////////////////////////////////////////
    '''
    # instantiate needed vars
    cvt = CVTools()
    displayPanel = Display()

    # HACK USER CHANGED VARS xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # backgroundSubK must be odd
    backgroundSubK = 255
    closeK = 25
    threshVal = 25

    # TODO make a loop function to run through all the files.

    for imageNumber in range (len(imgFileNames)):

        # load images to vars here. 0 is the gray mask
        # test (invasive cell), 6 (complicated), 3 (perfect)
        # 10.tif is the confocal
        # TODO fix image 8. seems to not work well with this
        imgFilePath = "img/" + imgFileNames[imageNumber]
        img_main = cv.imread(imgFilePath)
        img_main = cv.cvtColor(img_main, cv.COLOR_RGB2GRAY)
        orig = img_main.copy()
        # original image to draw on
        origDraw = img_main.copy()
        '''
        ////////////////////////////////////////////////////////////////////////////
        // Image Processing
        ////////////////////////////////////////////////////////////////////////////
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
        ////////////////////////////////////////////////////////////////////////////
        // Data Collection and Drawing
        ////////////////////////////////////////////////////////////////////////////
        '''

        # Data to collect
        '''
        * contour data ? this already gets collected though
        * light data at the specified points... make sure you handle background at some point
        '''

        # get contours, largest contour index, and the largest contour centroid
        imgContours = cvt.GetContours(dst3)
        largestContourIndex = cvt.GetLargestContour(imgContours)
        mainBodyCentroid = cvt.GetCentroid(imgContours[largestContourIndex])

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
            print("central point: " + str(mainBodyCentroid))
            d = cvt.GetDistanceBetween(mainBodyCentroid, offBodyCentroids[i])
            print(d)

            # add to array
            # TODO only if it is not 0,0 ghost centroid
            if (offBodyCentroids[i] != (0,0)):
                distancesFromCentroid.append(d)

                # visualize the offbody connection to the central location
                cvt.DrawOffBodyConnections(mainBodyCentroid, offBodyCentroids[i], origDraw)



            # draw centroids
            # cvt.DrawCentroid(origDraw, offBodyCentroids[i])

        # HACK get average dist from centroid
        # HACK get max dist from centroid






        # Data to draw
        '''
        * trace cell contours
        * draw centroids
        '''

        # trace the cell contours
        # NOTE: dst3 is the last processed image
        trace = cvt.DrawContours(dst3, origDraw, largestContourIndex)



        '''
        ////////////////////////////////////////////////////////////////////////////
        // Displaying Images
        ////////////////////////////////////////////////////////////////////////////
        '''
        # display images

        # toDisplay = [orig, dst, dst1, dst2, dst3, trace]


        # TODO turn the other images into BGR so they don't look terrible\
        # displayPanel.small_grid(toDisplay)
        # displayPanel.SingleView ("img", trace)


        '''
        TODO:
        * Would like to have a slider to drag to adjust blur and see the effect across all the images

        * click on matplot img to open up a cv imshow?
        '''



        '''
        ////////////////////////////////////////////////////////////////////////////
        // Write Output
        ////////////////////////////////////////////////////////////////////////////
        '''
        # use output handler to write the data to csv file
        output_handler.WriteData(m_csvFile, imgFileNames[imageNumber], distancesFromCentroid)

        # save images to output directory
        output_handler.SaveImage(trace, imgFileNames[imageNumber])
