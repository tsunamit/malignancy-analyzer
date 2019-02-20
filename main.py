import cv2 as cv
import numpy as np
import datetime
import time
import os                       # for path operations
import output_handler
from display import Display
from cvtools import CVTools

# Globals
FOLDER_TO_READ = "./../../Research/Data/proneural-mesenchymal/"
START_TIME = time.strftime("%Y%m%d-%H%M%")
OUTPUT_PATH = "./output/output-{}/".format(START_TIME)

backgroundSubK = 255 
closeK = 25
threshVal = 25

cvt = CVTools()
display_panel = Display()
img_file_names = []

image_of_interest = None
# image_of_interest = './../../Research/Data/proneural-mesenchymal/my2-4.tif'

def main():
    splash_screen()

    # Prep output environment
    output_handler.prep_output_environment(START_TIME)
    output_csv_name = "data.csv"
    output_csv_fd = open("{}{}".format(OUTPUT_PATH, output_csv_name), "w+")

    # Read folder image file names into array
    for subdir, dirs, files in os.walk(FOLDER_TO_READ):
        for file_name in files:
            img_file_names.append(file_name)
            print (file_name)

    # Run specific analysis on one image
    if (image_of_interest != None):
        print('Analyzing image of interest: {}'.format(image_of_interest))
        show_preprocessing_of_image(image_of_interest)
        return

    # Run analysis on each image
    img_analysis_data = []
    for i in range (len(img_file_names)):
        path = FOLDER_TO_READ + img_file_names[i]
        img_main = cv.imread(path)
        img_analysis_data.append(analyze_image(img_main, img_file_names[i]))
    output_handler.write_to_csv(output_csv_fd, img_analysis_data)
    return (0)


def analyze_image(img_main, img_name, show_preprocessing = False):
    print("Processing {}...".format(img_name))
    img_main = cv.cvtColor(img_main, cv.COLOR_RGB2GRAY) # Import image
    orig_draw = img_main.copy()      # Original image to draw on
    
    # Preprocess image
    dst = cvt.BackSub(img_main.copy(), backgroundSubK)
    dst1 = cvt.Close(dst, closeK)
    dst2 = cvt.Thresh(dst1, threshVal)
    dst2 = cvt.Close(dst2, 50)
    img_preproc = cvt.ImFill(dst2)

    # Data Collection and Drawing
    contours = []
    i_of_cell_sphere = None
    cell_sphere_shape_factor = None # circularity of cell sphere
    mig_contour_i_list = []
    mig_contours = []
    mig_centroids = []
    dists_from_cell_sphere = []
    num_mig_clusters = None
    avg_mig_cluster_size = None     # Average migration cluster size
    max_mig_dist = None             # Max migration distance

    contours = cvt.GetContours(img_preproc)
    i_of_cell_sphere = cvt.GetLargestContour(contours)
    cell_sphere_centroid = cvt.GetCentroid(contours[i_of_cell_sphere])

    # Get all other centroids, store in an array mig_centroids
    mig_contour_i_list = cvt.GetNonMainbodyContours(contours, 
        i_of_cell_sphere)
    for i in mig_contour_i_list:
        mig_contours.append(contours[i])
    for mig_contour in mig_contours:
        c = cvt.GetCentroid(mig_contour)
        mig_centroids.append(c)
    num_mig_clusters = len(mig_contours)

    # get the distance between the offbodies and the central centroid. Store in
    # an array
    for i in range(len(mig_centroids)):
        d = cvt.GetDistanceBetween(cell_sphere_centroid, mig_centroids[i])
        # Ignore a ghost centroids 
        # if (mig_centroids[i] != (0,0)):
        dists_from_cell_sphere.append(d)
        cvt.DrawOffBodyConnections(cell_sphere_centroid, 
            mig_centroids[i], orig_draw)
    max_mig_dist = max(dists_from_cell_sphere)
    avg_mig_cluster_size = np.mean(cvt.get_contour_areas(mig_contours))

    # Get shape factor
    cell_sphere_shape_factor = \
        cvt.get_shape_factor(contours[i_of_cell_sphere])

    
    # Create output images
    trace = None    # Shows contours traced and paths to migrating particles
    trace = cvt.DrawContours(img_preproc, orig_draw, i_of_cell_sphere)
    # trace = cvt.DrawContours(img_preproc, trace)

    # Show images with matplotlib
    # ====================================================
    if (show_preprocessing):
        display_panel.small_grid([img_main.copy(), dst1, dst2, img_preproc, trace])
        return
        # display_panel.SingleView("main", boxed)

    # Format output to csv
    # ====================================================
    data = [num_mig_clusters, cell_sphere_shape_factor, 
            max_mig_dist, avg_mig_cluster_size] 
    classification = get_classifier_from_filename(img_name)
    print("Done!")
    return format_obs_row(img_name, data, classification) 

    # Write Output
    # ====================================================
    # output_handler.save_image(trace, 'trace-{}'.format(img_name), OUTPUT_PATH)

# Formats a row of data for an observation. 
# out_f: fd  		csv file to write to 
# img_tag: string	img title for reference
# data: [] 			input values, 
# output_class int  class this observation belongs to
def format_obs_row(img_tag, data, output_class):
    row = []
    row.append(img_tag)	
    row = row + data
    row.append(output_class)
    return row

# Designed to show detailed analysis of preprocessing
def show_preprocessing_of_image(img_path):
    img = cv.imread(img_path)
    analyze_image(img, img_path, show_preprocessing = True)

# From the filename, return the class of cell
# 1. mesenchymal
# 2. proneural
def get_classifier_from_filename(img_name):
    if ("m" in img_name):
        return 1
    if ("p" in img_name):
        return 2

def splash_screen():
    print("CREATOR: tsunamit\n" + "OPENCV " + cv.__version__)
    print('RUNTIME: ' + (str)(datetime.datetime.now()))
    print("/\n/\n/\nRUNNING\n/\n/\n/\n")


if __name__ == "__main__":
    main()