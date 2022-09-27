import tkinter as tk
from tkinter import tix
import dbOrNotdb as dbUtility


class prosthikiHander(tk.Tk):

    def __del__(self):

        print("Ending Phase_1")

    def __init__(self,master):
        #reference to window class as master
        print(self)
        self.master = master
        self.master.ntestroy(self)
