import tkinter as tk
from tkinter import tix
#import pyperclip
import dbOrNotdb as dbUtility
import scrollableFrame as scrollableFrame

#self.tip = tix.Balloon(self.master.window)
#self.master.tip.bind_widget(but, balloonmsg = keimeno)
#                but = tk.Button(frame.interior, text = title, justify = "center",width = 15, wraplength = 100, command = lambda x = keimeno : pyperclip.copy(x) )
class epilogesHander(tk.Tk):

    def __del__(self):
        print("Ending epiloges")

    def __init__(self,master):
        #reference to window class as master
        self.master = master
        self.master.ntestroy(self)

        self.katigories = buttonList(self,\
        "SELECT * FROM Katigoria where id <> ?",\
        "delete Katigories")
        self.themata = buttonList(self,\
        "select f.id, t.desc from (FramesKatigorias as f left Join Thema as t on t.id = f.themaId) where f.katigoriaId = ?",\
        "delete Themata")
        self.keimena = proboliKeimenou(self,"select b.keimenaId,k.title,k.desc from (Buttons as b left Join Keimena as k on k.id = b.keimenaId) where b.themaKatigoriasId = ?",\
        "delete proboliKeimenou")

        self.katigories.slaveList = self.themata
        self.themata.slaveList = self.keimena

        self.katigories.createBut(-1)

class proboliKeimenou(tk.Tk):

    def __del__(self):
        print(self.delMsg)

    def __init__(self,master,query, delMsg):
        self.master = master
        self.query = query
        self.delMsg = delMsg
        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#ffffff", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "both", expand = True, anchor = "nw")

    def createBut(self, id):
        self.scrolledFrame = scrollableFrame.VerticalScrolledFrame(self.frame)
        self.scrolledFrame.configure(borderwidth = 5, relief = "ridge")
        self.scrolledFrame.pack(fill = "both",expand = True)

        butList = dbUtility.get(self.master.master.path,(self.query,(id,)))
        row = 0
        column = 0
        for widget in butList:
            id,title,keimeno = widget
            if keimeno != None:
                but = tk.Button(self.scrolledFrame.interior,text = title, padx = 3, pady = 3, relief = "raised", justify = "center",width = 15, wraplength = 100, command = lambda x = keimeno : pyperclip.copy(x))

                but.grid(row = row, column = column, padx = 3, pady = 3, ipadx = 5, ipady = 5)

                column += 1
                if column > 4:
                    row += 1
                    column = 0


    def deleteBut(self):
        for item in self.frame.winfo_children():
            item.destroy()

class buttonList(tk.Tk):

    def __del__(self):
        print(self.delMsg)

    def __init__(self,master,query,delMsg):
        self.master = master
        self.query = query
        self.delMsg = delMsg
        self.slaveList = None
        self.but = {}
        self.value = None


        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#b9b5b5", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "y", anchor = "nw")

    def createBut(self, id):

        self.scrolledFrame = scrollableFrame.VerticalScrolledFrame(self.frame)
        self.scrolledFrame.configure(borderwidth = 5, relief = "groove")
        self.scrolledFrame.pack(fill = "y", expand =True)

        butList = dbUtility.get(self.master.master.path,(self.query,(id,)))

        for widget in butList:
            id,title = widget
            but = tk.Button(self.scrolledFrame.interior, width = 20, wraplength = 100,  justify = "left", text = title, command = lambda x = id, y = title : self.butFunction(x,y), relief = "groove")
            but.pack(side = "top", fill = "x")
            self.but[id] = but

    def butFunction(self,id,title):
        if self.value != None:
            self.but[self.value].configure(state = "normal")

        self.but[id].configure(state = "disabled")

        self.value = id

        self.slaveList.deleteBut()
        self.slaveList.createBut(id)

    def deleteBut(self):
        for item in self.frame.winfo_children():
            item.destroy()
        self.slaveList.deleteBut()
        self.but.clear()
        self.value = None
