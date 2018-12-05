import cv2 as cv
import numpy as np
import datetime
import os                       # for path operations
import output_handler
from display import Display
from cvtools import CVTools


# CONSTANTS
# HACK USER CHANGED VARS xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# backgroundSubK must be odd
#
# FOLDER_TO_READ = "./videoimg/"
FOLDER_TO_READ = "./img/"

DEF_BACKGROUNDSUB_K = 255
DEF_CLOSE_K = 25
DEF_THRESH_VAL = 25

backgroundSubK = 255
closeK = 25
threshVal = 25

# instantiate needed vars
cvt = CVTools()
displayPanel = Display()
imgFileNames = []

def SplashScreen():
    print("CREATOR: tsunamit\n" + "OPENCV " + cv.__version__)
    print('RUNTIME: ' + (str)(datetime.datetime.now()))
    print("/\n/\n/\nRUNNING\n/\n/\n/\n")


def AnalyzeOneImage(img_main, imageNumber = 0):
    img_main = cv.cvtColor(img_main, cv.COLOR_RGB2GRAY)
    orig = img_main.copy()
    # original image to draw on
    origDraw = img_main.copy()

    # PROCESS IMAGE

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
    # cvt.applyFft(dst3)

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
        # print ("offpoint: " + str(offBodyCentroids[i]))
        # print("central point: " + str(mainBodyCentroid))
        d = cvt.GetDistanceBetween(mainBodyCentroid, offBodyCentroids[i])
        # print(d)

        # add to array
        # TODO only if it is not 0,0 ghost centroid
        if (offBodyCentroids[i] != (0,0)):
            distancesFromCentroid.append(d)

            # visualize the offbody connection to the central location
            cvt.DrawOffBodyConnections(mainBodyCentroid, offBodyCentroids[i], origDraw)

        # draw centroids
        # cvt.DrawCentroid(origDraw, offBodyCentroids[i])

    # trace the cell contours

    # NOTE: dst3 is the last processed image
    trace = cvt.DrawContours(dst3, origDraw, largestContourIndex)
    # trace = cvt.DrawContours(dst3, origDraw)

    boxed = cvt.boxLargestContour(trace, imgContours[largestContourIndex])
    orig_boxed = cvt.boxLargestContour(orig, imgContours[largestContourIndex])
    # Apply fft to boxed
    fftData = cvt.applyFft(orig_boxed)

    fftImg = displayPanel.retrieveFftImg(fftData)
    # Inverted version of fft (black with white dots)
    # fftImg = (255 - displayPanel.retrieveFftImg(fftData))

    quads = cvt.fold_quadrants(fftImg)

    # displayPanel.SingleView("main", trace)
    # displayPanel.SingleView("main", boxed)
    # displayPanel.small_grid([orig, dst1, dst2, dst3, boxed])

    '''
    ////////////////////////////////////////////////////////////////////////////
    // Write Output
    ////////////////////////////////////////////////////////////////////////////
    '''
    #
    # # use output handler to write the data to csv file
    # output_handler.WriteData(m_csvFile, imgFileNames[imageNumber], distancesFromCentroid)
    #
    # # save images to output directory
    output_handler.SaveImage(fftImg, imgFileNames[imageNumber])
    output_handler.SaveImage(boxed, 'box' + imgFileNames[imageNumber])
    for i in range (4):
        output_handler.SaveImage(quads[i], imgFileNames[imageNumber] + 'quad' + str(i) + '.tif')

def run():

    SplashScreen()

    f = open("log.txt", "w+")
    # HACK make new log files each run!!!!
    m_csvFile = open("data.csv", "w+")

    # prep output enviro
    output_handler.PrepOutputEnvironment()

    '''
    ////////////////////////////////////////////////////////////////////////////
    // SELECT IMAGE DIRECTORY
    ////////////////////////////////////////////////////////////////////////////
    '''

    # want to specitfy a path here
    for subdir, dirs, files in os.walk(FOLDER_TO_READ):
        for fileName in files:
            imgFileNames.append(fileName)
            print (fileName)


    '''
    ////////////////////////////////////////////////////////////////////////////
    // Variables
    ////////////////////////////////////////////////////////////////////////////
    '''


    # TODO make a loop function to run through all the files.

    for imageNumber in range (len(imgFileNames)):

        # load images to vars here. 0 is the gray mask
        # test (invasive cell), 6 (complicated), 3 (perfect)
        # 10.tif is the confocal
        # TODO fix image 8. seems to not work well with this
        imgFilePath = FOLDER_TO_READ + imgFileNames[imageNumber]
        img_main = cv.imread(imgFilePath)
        AnalyzeOneImage(img_main, imageNumber)


'''
////////////////////////////////////////////////////////////////////////////
// Run Program
////////////////////////////////////////////////////////////////////////////
'''
run()
