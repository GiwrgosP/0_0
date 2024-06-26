import tkinter as tk
import os
import dbOrNotdb as dbUtilit
from tkinter import tix
from tkinter.ttk import *

import epiloges
#import anazitisi
import prosthiki
import new
import change
import eksagwgi
import quit

#window object
class syzygyWindow(tk.Tk):

    menuOptions = { "ΕπιλοYes" : {"Δεδομένα": epiloges.epilogesHander,
                                "Προσθήκη": new.newHander,
                                "Τροποποίηση": change.changeHander,
                                "Εξαγωγή": eksagwgi.eksagwgiHander},

                    "Έξοδος": {"ΕΞΟΔΟΣ": quit.quitHander}
    }

    def __del__(self):
        print("Ending")

    def __init__(self):
        #find the path of the current file
        self.path = os.path.dirname(os.path.abspath(__file__))
        #create a window object
        self.window = tix.Tk()
        #name it
        self.window.title("Syzygy")
        #size it
        self.window.geometry("1200x600")
        #icon it
        iconPath = self.path + "\icon.ico"
        self.window.iconbitmap(iconPath)
        #variable with the menu option submenu
        self.state = None

        self.createMainFrame()
        self.createMenuBar()

    def createMainFrame(self):
        self.mainFrame = tk.Frame(self.window,bg = "#b9b5b5")
        self.mainFrame.pack(fill = "both", expand = True)


    #itarate the menuOptions dictionary to create the menus and the submenus of the menu bar
    def createMenuBar(self):
        self.menuBar = tk.Menu(self.window)
        for menu, options in self.menuOptions.items():
            newMenu = tk.Menu(self.menuBar, tearoff=0)

            for subMenu, action in options.items():
                newMenu.add_command(label=subMenu, command=lambda action=action: action(self))

            self.menuBar.add_cascade(label=menu, menu=newMenu)

        self.window.config(menu=self.menuBar)

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
    root = syzygyWindow()
    root.window.mainloop()

#call the main function
main()
