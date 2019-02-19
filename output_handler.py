'''****************************************************************************************************
output.py
handles the output of data to (in this case) a csv file
****************************************************************************************************'''

import csv 		# csv library
import cv2 as cv
import os
import errno

	
# Write data matrix to csv file f
def write_to_csv(f, data):
	print("Writing data to csv file")
	print("...")
	writer = csv.writer(f)
	writer.writerows(data)
	print("Done!")


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
Manage/Create Output Folder:
-------------------------
Creates the output folder if it doesn't exist. If it exists already don't do anything
'''
def prep_output_environment(start_time):
	try:
		os.mkdir('./output/')
	except OSError as e:
		if e.errno == errno.EEXIST:
			print("OutputHandler: output folder already created. Doing nothing...")
		else:
			raise	# raise exception if it is not the not exist error
	try:
		os.mkdir('./output/output-{}/'.format(start_time))
	except OSError as e:
		print("Something weird is happening. Find me...")


'''
Save Image to output folder:
-------------------------
save image into an output folder to view later
'''
def save_image(image_to_save, file_name, output_path):
	print ("Writing {} to {}".format(file_name, output_path))
	cv.imwrite((output_path + file_name), image_to_save)
	print ("Done\n")
