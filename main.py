import tkinter as tk
import os
import epiloges
import prosthiki
import eksagwgi
import dbOrNotdb as dbUtilit
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
        self.window.geometry("1200x600")
        iconPath = self.path + "\icon.ico"
        self.window.iconbitmap(iconPath)
        self.state = None

        self.createMainFrame()
        self.createMenuBar()


    #crete Main Frame
    def createMainFrame(self):
        self.mainFrame = tk.Frame(self.window,bg = "#b9b5b5")
        self.mainFrame.pack(fill = "both", expand = True)

    def createMenuBar(self):
        self.menuBar = tk.Menu(self.window)

        utilityMenu = tk.Menu(self.menuBar, tearoff = 0)
        utilityMenu.add_command(label = "Δεδομένα", command = lambda: epiloges.epilogesHander(self) )
        utilityMenu.add_command(label = "Προσθήκη", command = lambda: prosthiki.prosthikiHander(self) )
        utilityMenu.add_command(label = "Εξαγωγή", command = lambda: eksagwgi.eksagwgiHander(self) )

        self.menuBar.add_cascade(label = "ΕπιλοYes",  menu = utilityMenu)

        exitMenu = tk.Menu(self.menuBar, tearoff=0)
        exitMenu.add_command(label="ΕΞΟΔΟΣ",command = lambda :quit())
        self.menuBar.add_cascade(label="ΕΞΟΔΟΣ", menu=exitMenu)

        self.window.config(menu =  self.menuBar)

    def ntestroy(self,slave):
        for item in self.mainFrame.winfo_children():
            item.destroy()
        try:
            self.state.__del__()
            print("destroyed")
        except:
            pass

        self.state = slave



def main():
    root = window()
    root.window.mainloop() 

#call the main function
main()
