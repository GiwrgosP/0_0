import tkinter as tk
import os
import phase_1
import phase_2
import dbOrNotdb as dbUtility
from tkinter import tix
from tkinter.ttk import *

#window object
class window(tk.Tk):
    def __del__(self):

        print("Ending")

    def __init__(self):
        #find the path of the current file
        self.path = os.path.dirname(os.path.abspath(__file__))
        #make the fileSelected paremeter equal to None
        #create a window object
        self.window = tix.Tk()
        #name it
        self.window.title("Syzygy")
        #size it
        self.window.geometry("1536x768")
        iconPath = self.path + "\icon.ico"
        self.window.iconbitmap(iconPath)
        self.phase = ""
        self.katigoriaId = -1
        self.createWindow()


    def createWindow(self):

        self.mainFrame = tk.Frame(self.window,bg = "#5ef292")
        self.createKatigoriaSection()
        self.mainFrame.pack(fill = "both", expand = True)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=0)
        self.mainFrame.rowconfigure(0, weight=0)
        self.mainFrame.rowconfigure(1, weight=1)


    def createKatigoriaSection(self):
        try:
            self.katigoriaFame.destroy()
            self.utilityFrame.destroy()
        except:
            pass
        self.katigoriaButtons = {}
        self.katigoriaFrame = tk.Frame(self.mainFrame, bg = "#ccccff", borderwidth = 5, relief = "groove")
        self.utilityFrame = tk.Frame(self.mainFrame, bg = "#cce0ff", borderwidth = 5, relief = "groove")
        katigoriaList = dbUtility.get(self.path,("SELECT * FROM Katigoria",list()))
        col = 0
        row = 0
        for katigoria in katigoriaList:
            id,title = katigoria
            self.katigoriaButtons[id] = tk.Button(self.katigoriaFrame,text = title, command = lambda x = id : self.checkState(x,"phase_1"))
            self.katigoriaButtons[id].grid(column = col,row = row)
            if col == 4:
                col = 0
                row += 1
            else:
                col += 1


        self.katigoriaButtons[-1] = tk.Button(self.utilityFrame,text = "Προσθήκη Νέων",command = lambda x = -1 : self.checkState(x,"phase_2"))
        self.katigoriaButtons[-1].grid()

        self.katigoriaFrame.columnconfigure(0, weight=1)
        self.katigoriaFrame.columnconfigure(1, weight=1)
        self.katigoriaFrame.columnconfigure(2, weight=1)
        self.katigoriaFrame.columnconfigure(3, weight=1)
        self.katigoriaFrame.columnconfigure(4, weight=1)

        self.utilityFrame.columnconfigure(0, weight=1)
        self.utilityFrame.columnconfigure(1, weight=1)

        self.katigoriaFrame.grid(row = 0, column = 0, sticky = "ewns")
        self.utilityFrame.grid(row = 0, column = 1, sticky = "ewns")

        if self.phase != "":
            self.checkState(self.katigoriaId,self.phase)



    def checkState(self,id,phase):

        self.phase = phase
        self.katigoriaId = id
        try:
            self.selection.__del__()
        except:
            print("NO Selection Object")

        if phase == "phase_1":
            self.selection = phase_1.windowHander(self)
            for but in self.katigoriaButtons:
                if but == id:
                    self.katigoriaButtons[but].configure(state = "disabled")
                else:
                    self.katigoriaButtons[but].configure(state = "normal")

        elif phase == "phase_2":
            self.selection = phase_2.windowHander(self)
            for but in self.katigoriaButtons:
                self.katigoriaButtons[but].configure(state = "normal")
        print("end Selection")


def main():
    root = window()
    root.window.mainloop()

#call the main function
main()
