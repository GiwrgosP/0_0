import tkinter as tk
from tkinter import tix
import dbOrNotdb as dbUtility
import scrollableFrame as scrollableFrame

import buttonList as buttonList


class epilogesHander():

    def __del__(self):
        print("Ending epiloges")

    def __init__(self,master):
        #reference to window class as master
        self.master = master
        self.master.ntestroy(self)
        self.tip = tix.Balloon(self.master.window)

        self.katigories = buttonList.buttonList(self,\
        "SELECT * FROM Katigoria where id <> ?",\
        "delete Katigories")
        self.themata = buttonList.buttonList(self,\
        "select f.id, t.desc from (FramesKatigorias as f left Join Thema as t on t.id = f.themaId) where f.katigoriaId = ?",\
        "delete Themata")
        self.keimena = proboliKeimenou(self,"select b.keimenaId,k.title,k.desc from (Buttons as b left Join Keimena as k on k.id = b.keimenaId) where b.themaKatigoriasId = ?",\
        "delete proboliKeimenou")

        self.katigories.slaveList = self.themata
        self.themata.slaveList = self.keimena

        self.katigories.createButtonList(-1)

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

                self.master.tip.bind_widget(but, balloonmsg = keimeno)

                column += 1
                if column > 4:
                    row += 1
                    column = 0


    def deleteBut(self):
        for item in self.frame.winfo_children():
            item.destroy()
