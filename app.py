# import main
# import cv2 as cv
# import numpy as np
# import datetime
# import os                       # for path operations
# import output_handler
from display import Display
from cvtools import CVTools
import tkinter as tk

root  = tk.Tk()
frame = tk.Frame(root)
frame.pack()

# slider
slider = tk.Scale(root, from_= 0, to = 42, orient = tk.HORIZONTAL)

# runButton = tk.Button(frame, text = 'START', command = main.run)
button = tk.Button(frame, text = "QUIT", fg = "red", command = quit)
# runButton.pack(side = tk.TOP)
button.pack(side = tk.LEFT)
slider.pack()

root.mainloop()
