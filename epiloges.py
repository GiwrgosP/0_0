import tkinter as tk
from tkinter import tix
import pyperclip
import dbOrNotdb as dbUtility


class epilogesHander(tk.Tk):

    def __del__(self):
       print("Ending Phase_1")

    def __init__(self,master):
        try:
            self.frameKatigories.destroy()
            self.themataKeimenaFrame.destroy()
        except:
            pass
        #reference to window class as master
        self.master = master

        self.tip = tix.Balloon(self.master.window)
        self.createKatigoriesFrame()

    def createKatigoriesFrame(self):
        self.frameKatigories = tk.Frame(self.master.mainFrame, bg = "#ffffff", borderwidth = 5, relief = "groove")

        katigoriesList = dbUtility.get(self.master.path,("SELECT * FROM Katigoria",list()))
        row =  0
        for kat in katigoriesList:
             id,title = kat
             but = tk.Button(self.frameKatigories, width = 20, wraplength = 100,  justify = "left", text = title, command = lambda x = id : self.createKeimenaFrame(x))
             but.grid(column  = 0, row = row,sticky = "ew")
             row += 1

        self.frameKatigories.pack(side = "left", fill = "y", anchor = "nw")

    def createKeimenaFrame(self,id):
        try:
            self.themataKeimenaFrame.destroy()
        except:
            pass

        self.themataKeimenaFrame= tk.Frame(self.master.mainFrame, bg = "#ffffff", borderwidth = 5, relief = "groove")

        themataList = dbUtility.get(self.master.path,("SELECT id,themaId FROM FramesKatigorias WHERE katigoriaId = ?", (id,)))

        for thema in themataList:
            themaKatigoriaId,  themaId = thema
            themaTitle, themaColor = dbUtility.get(self.master.path,("SELECT desc,colorCode FROM Thema WHERE id = ?",(themaId,)))[0]

            frame = tk.Frame(self.themataKeimenaFrame, bg = themaColor, borderwidth = 5, relief = "groove")

            label = tk.Label(frame, text = themaTitle, justify = "left",  relief = "groove", padx = 5, pady = 5, borderwidth = 10)
            label.grid(column = 0, row = 0, sticky = "ewns")

            keimenaThematosKatigorias = dbUtility.get(self.master.path,("SELECT id,keimenaId FROM Buttons WHERE themaKatigoriasId = ?",(themaKatigoriaId,)))

            row = 0
            column = 1

            for keimeno in keimenaThematosKatigorias:
                garbage, keimenoId =  keimeno
                title, keimeno = dbUtility.get(self.master.path,("SELECT title,desc FROM Keimena WHERE id = ?",(keimenoId,)))[0]
                but = (tk.Button(frame, text = title, justify = "center",width = 15, wraplength = 100, command = lambda x = keimeno : pyperclip.copy(x) ))
                self.tip.bind_widget(but, balloonmsg = keimeno)
                but.grid(column = column, row = row)
                if column >= 5:
                    column = 1
                    row += 1
                else:
                    column += 1

            frame.pack(fill = "x")
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)
            frame.columnconfigure(3, weight=1)
            frame.columnconfigure(4, weight=1)
            frame.columnconfigure(5, weight=1)
            frame.columnconfigure(6, weight=1)
            for r in range(row):
                frame.rowconfigure(r, weight=1)

        self.themataKeimenaFrame.pack(side = "left", fill = "both", expand = True)
        self.themataKeimenaFrame.columnconfigure(0, weight=1)
        self.themataKeimenaFrame.columnconfigure(1, weight=0)
