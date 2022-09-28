import tkinter as tk
from tkinter import tix
import dbOrNotdb as dbUtility


class prosthikiHander(tk.Tk):

    def __del__(self):

        print("Ending Phase_1")

    def __init__(self,master):

        self.master = master
        self.master.ntestroy(self)

        self.katigories = katigories(self)
        self.themata = themata(self,None)
        self.keimena = keimena(self, None)

    def checkState(self,id):
        pass



class katigories(tk.Tk):

    def __init__(self,master):
        self.master = master
        self.but = {}
        self.value = None
        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#ffffff", borderwidth = 5, relief = "groove")

        katigories = dbUtility.get(self.master.master.path,("SELECT * FROM Katigoria",list()))

        for kat in katigories:
            id,title = kat

            but = tk.Button(self.frame, width = 20, wraplength = 100,  justify = "left", text = title, command = lambda x = id : self.butFunction(x))
            but.pack(side = "top", fill = "x")

            self.but[id] = but

        self.frame.pack(side = "left", fill = "y", anchor = "nw")


    def butFunction(self,id):
        del self.master.themata
        try:
            self.but[self.value].configure(state = "normal")
        except:
            pass
        self.but[id].configure(state = "disabled")
        self.value = id
        self.master.checkState(id)
        self.master.themata = themata(self.master,id)

class themata(tk.Tk):

    def __del__(self):
        print("del thema")
        self.frame.destroy()
        del self.master.keimena

    def __init__(self,master,katigoriaId):
        self.master = master
        self.but = {}
        self.value = None
        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#ffffff", borderwidth = 5, relief = "groove")

        themata = dbUtility.get(self.master.master.path,("select t.id, t.desc from (FramesKatigorias as f left Join Thema as t on t.id = f.themaId) where f.katigoriaId = ?",(katigoriaId,)))

        for them in themata:
            id,title = them

            but = tk.Button(self.frame, width = 20, wraplength = 100,  justify = "left", text = title, command = lambda x = id : self.butFunction(x))
            but.pack(side = "top", fill = "x")

            self.but[id] = but

        self.frame.pack(side = "left", fill = "y", anchor = "nw")

    def butFunction(self,id):

        if self.value != None:
            try:
                del self.master.keimena
            except:
                pass
            self.but[self.value].configure(state = "normal")

        self.but[id].configure(state = "disabled")
        self.value = id
        self.master.checkState(id)


class keimena(tk.Tk):
    def __del__(self):
        self.frame.destroy()

    def __init__(self,master,id):
        self.master = master
        self.but = None
        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#ffffff", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "y", anchor = "nw")
