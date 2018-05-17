# Malignancy Detector
Using Python with OpenCV, program processes microscope images of cancer cell colonies and quantifies malignancy based on defined set of parameters from migration patterns and form factor. All output dumped as images to ./output/ and all numerical data saved (per program run) in data.csv. Program created for Seidlits Research Group -- Bioengineering Dept, UCLA.

## Features Extracted (Currently)
* Main cell colony identification and contour trace
* Main cell colony shape factor (circularity)
* Migrating particle identification and contour trace
* Identification and labeling of main cell colony, and migrating cell centroids
* Migrating cell count
* Migrating cell distance from main body centroid


## Bugs
* image 8 imfill process deletes the blob we actually detected.

## TODO later
* add distance to contour for migrating particles
* use a faster algorithm (making use of the hierarchy) to search for the largest contour


### Libraries Used
* OpenCV 3.4.0
* NumPy
* MatplotLib
* Tkinter
