'''****************************************************************************************************
output.py 
handles the output of data to (in this case) a csv file
****************************************************************************************************''' 

import csv 		# csv library
import cv2 as cv


'''
Write Data: 
-------------------------
writes relevant data into csv file
'''
def WriteData(m_csvFile, imgName, offBodyDistances):
	'''
	m_csvFile : 					m_csvFile to write to 
	imgName, 						String: name of image
	offBodyDistances, list<double>: distances from center centroid
	'''

	# create writer object
	csvWriter = csv.writer(m_csvFile)

	# write a test line
	csvWriter.writerow([imgName])
	csvWriter.writerow(["count"] + [len(offBodyDistances)])

	# write rows for each migrating point
	for i in range (len(offBodyDistances)):

		# for each offBodyDistance[i], get the name and writerow with name and distance
		name = "m" + str(i+1)

		csvWriter.writerow([name] + [offBodyDistances[i]])

	csvWriter.writerow('')
	csvWriter.writerow('')


	# start new entry with a new line

'''
Save Image to output folder: 
-------------------------
save image into an output folder to view later
'''
def SaveImage(imageToSave, fileName):
	outputDirPath = "./output/"
	cv.imwrite((outputDirPath + fileName), imageToSave)
