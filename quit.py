import tkinter as tk

class quitHander(tk.Tk):
    def __init__(self,master):
        self.master = master
        self.master.ntestroy(self)
        self.master.window.quit()
        print("Quit")
