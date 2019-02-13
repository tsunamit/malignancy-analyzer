'''******************************************************
Delete all files in directory except for the extension we want
******************************************************'''

import os

files_to_test = os.listdir("./")

for item in files_to_test:
	if (item.endswith(".tif") == False):
		# ends up deleting itself which is kind of cool since we don't want it in there anyways!
		os.remove(os.path.join("./", item))
		print(item + " was deleted!")
