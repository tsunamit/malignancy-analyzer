import numpy as np
import cv2 as cv
import os
import errno

filepath = 'data/HK217-RGD-Full 48hr_E4_4.mp4'
output_path = './videoimg/'

cap = cv.VideoCapture(filepath)
frames = []

while (cap.isOpened()):
    ret, frame = cap.read()

    if (ret == True):
        cv.imshow('frame',frame)
        frames.append(frame)
        print("frame stored")
    else:
        break

    if cv.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv.destroyAllWindows()

print("trying to save...")


try:
	os.mkdir(output_path)
	print("OutputHandler: output folder created...")
except OSError as e:
	if e.errno == errno.EEXIST:
		print("OutputHandler: output folder already created. Doing nothing...")
	else:
		raise	# raise exception if it is not the not exist error

for i in range(len(frames)):
    cv.imwrite((output_path + str(i) + ".jpg"), frames[i])
