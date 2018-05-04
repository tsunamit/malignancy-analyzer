import tkinter as tk
import main

root  = tk.Tk()
frame = tk.Frame(root)
frame.pack()

runButton = tk.Button(frame, text = 'START', command = main.run)
button = tk.Button(frame, text = "QUIT", fg = "red", command = quit)
runButton.pack(side = tk.TOP)
button.pack(side = tk.LEFT)

root.mainloop()
