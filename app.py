from tkinter import *
import main


class AppInterface:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        # Button 1: analyze one images
        self.analyzeOneButton = Button(frame, text = "Analyze One", command = self.AnalyzeOne)
        self.analyzeOneButton.pack(side = TOP)

        # Button 2: analyze all images (after selection)
        self.analyzeOneButton = Button(frame, text = "Analyze All", command = self.AnalyzeAll)
        self.analyzeOneButton.pack(side = TOP)

        # Button 3: quit
        self.quitButton = Button(frame, text = "Quit", fg = "red", command = quit)
        self.quitButton.pack(side = BOTTOM)


    def AnalyzeOne(self):
        print("Analyzing one ... ")


    def AnalyzeAll(self):
        print("Analyzing all ... ")
        main.run()


'''
# slider
slider = tk.Scale(root, from_= 0, to = 255, orient = tk.HORIZONTAL)
slider.pack()
'''

root = Tk()
myApp = AppInterface(root)
root.mainloop()
