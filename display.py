import cv2 as cv
import numpy as np

# saved my life
import matplotlib
matplotlib.use("TkAgg")

from matplotlib import pyplot as plt

'''
Display Class
Handles the matplotlib outputs and formatting
'''
class Display:

    '''
    Plot
    -------------------------
    plt.show() with adjustments
    removed all whitespace between images and maximized the image span across the window
    '''
    def Plot(self):
        plt.subplots_adjust(wspace = 0, hspace = 0, left = 0, right = 1, bottom = 0.0, top = 1.0)
        plt.show()

    '''
    Show Small Grid
    -------------------------
    Image display method for 2x3 matrix of images. So 6 mats max
    '''
    def small_grid(self, imgs):
        if len(imgs) > 6:
            print('Too many images. Only accepts max 6')
        else:
            plt.figure(1)
            for i in range(len(imgs)):
                plt.subplot(231+i)
                plt.imshow(imgs[i])
                plt.xticks([])
                plt.yticks([])


            self.Plot()

    '''
    Large Image Display Comparison
    -------------------------
    1x2 matrix array of images
    '''
    def large_compare(self, img):
        if len(img) == 2:
            plt.figure(2)
            for i in range(len(img)):
                plt.subplot(121+i)
                plt.imshow(img[i])
                plt.xticks([])
                plt.yticks([])
        else:
            print('not enough images to compare')
        self.Plot()


    '''
    Single Image Display
    -------------------------
    imopen method of openCV to display image
    '''
    def SingleView(self, winname, img):
        if img is not None:
            cv.namedWindow(winname, cv.WINDOW_KEEPRATIO)

            cv.createTrackbar("Close Kernel", winname, 0, 100, self.nothing)

            cv.imshow(winname, img)
            cv.waitKey(0)


    def nothing(self):
        print("changed")
        pass
