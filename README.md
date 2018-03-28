# Malignancy Detector
Sorts microscope images of cancer cells as aggressive or nonaggressive using Python and OpenCV. Program to be employed for a specific assay in UCLA bioengineering research lab. Determines malignancy and migratory aptitude from the shape factor of the cell sphere outline.

## Current Tasklist
* get a set of vertices for circles with a specified radii

## Bugs
* image 8 imfill process deletes the blob we actually detected.

## TODO later
* use a faster algorithm (making use of the hierarchy) to search for the largest contour


### Libraries Used
* OpenCV 3.4.0
* NumPy
* MatplotLib
* Tkinter
* XlsxWriter
