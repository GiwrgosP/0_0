import tkinter as tk
from operator import itemgetter
import pyperclip
import dbOrNotdb as dbUtility
from tkinter import tix
from tkinter import tix

class windowHander(tk.Tk):
    def __del__(self):
        self.frame.destroy()
        print("Ending Phase_1")

    def keimenoCallBack(self,*args):
        k = self.addKeimeno.get()
        frameKarigorias,keimenoId,garbage = k.split("*")
        dbUtility.add(self.master.path,("INSERT INTO Buttons (themakatigoriasId,keimenaId) VALUES (?,?)", (int(frameKarigorias),int(keimenoId))))
        self.master.checkState(self.master.katigoriaId, self.master.phase)

    def themaCallBack(self,*args):
        k = self.addThema.get()
        katigoriaId,themaId,garbage = k.split("*")
        dbUtility.add(self.master.path,("INSERT INTO FramesKatigorias (katigoriaId,themaId) VALUES (?,?)", (int(katigoriaId),int(themaId))))
        self.master.checkState(self.master.katigoriaId, self.master.phase)

    def deleteBut(self,id):
        dbUtility.add(self.master.path,("DELETE FROM Buttons WHERE id = ?", (int(id),)))
        self.master.checkState(self.master.katigoriaId, self.master.phase)

    def deleteThem(self,id):
        dbUtility.add(self.master.path,("DELETE FROM Buttons WHERE themakatigoriasId = ?", (int(id),)))
        dbUtility.add(self.master.path,("DELETE FROM FramesKatigorias WHERE id = ?", (int(id),)))
        self.master.checkState(self.master.katigoriaId, self.master.phase)

    def __init__(self,master):
        #reference to window class as master
        self.master = master
        self.addKeimeno = tk.StringVar()
        self.addThema = tk.StringVar()

        self.frame = tk.Frame(self.master.mainFrame,borderwidth = 5, relief = "groove")

        self.frameList = list()
        self.buttonList = list()

        self.tip = tix.Balloon(self.master.window)

        self.createKatigoriaShow()

        self.frame.grid(column = 0, row = 1, sticky = "ewns", columnspan = 2)

        self.trace = self.addKeimeno.trace_add('write', self.keimenoCallBack)
        self.trace = self.addThema.trace_add('write', self.themaCallBack)


    def createKatigoriaShow(self):
        frameList = dbUtility.get(self.master.path,("SELECT id,themaId FROM FramesKatigorias WHERE katigoriaId = ?", (self.master.katigoriaId,)))
        self.createAddThema(frameList,1)

        for frame in frameList:
            frameId, themaId = frame

            text,color = dbUtility.get(self.master.path,("SELECT desc,colorCode FROM Thema WHERE id = ?",(themaId,)))[0]

            self.frameList.append(tk.Frame(self.frame,bg = color, borderwidth = 3, relief = "groove"))


            label = tk.Label(self.frameList[-1], text = text )
            label.pack(side = "left",padx=2, pady=2)

            buttonList = dbUtility.get(self.master.path,("SELECT id,keimenaId FROM Buttons WHERE themaKatigoriasId = ?",(frameId,)))
            allKeimena = dbUtility.get(self.master.path,("SELECT * FROM Keimena",list()))
            for but in buttonList:

                id, keimenaId = but
                title,desc = dbUtility.get(self.master.path,("SELECT title,desc FROM Keimena WHERE id = ?",(keimenaId,)))[0]

                self.buttonList.append(tk.Button(self.frameList[-1], text = title, command = lambda x = desc : pyperclip.copy(x) ))
                self.buttonList[-1].pack(side = "left",padx=2, pady=2)
                self.tip.bind_widget(self.buttonList[-1], balloonmsg = desc)
                flag = True
                for i in range(len(allKeimena)):
                    if allKeimena[i][0] == keimenaId:
                        flag = False
                        break
                if flag == False:
                    allKeimena.pop(i)

                self.buttonList.append(tk.Button(self.frameList[-1], text = "x", command = lambda x = id : self.deleteBut(x)))
                self.buttonList[-1].pack(side = "left")

            self.keimenoMenu = tk.Menubutton(self.frameList[-1], text = "Προσθήκη Κειμένου",borderwidth = 3, relief = "groove")
            self.keimenoMenu.menu = tk.Menu(self.keimenoMenu)
            self.keimenoMenu["menu"] = self.keimenoMenu.menu

            for val in allKeimena:
                l = str(frameId) + "*" + str(val[0]) + "*" + val[1]
                self.keimenoMenu.menu.add_radiobutton(label = l, value = l, variable = self.addKeimeno)

            self.deleteThema = tk.Button(self.frameList[-1], text = "x", command = lambda x = frameId : self.deleteThem(x))
            self.deleteThema.pack(side = "right", padx=5, pady=5)
            self.keimenoMenu.pack(side = "right", padx=5, pady=5)

            self.frameList[-1].pack(side = "top", fill = "x", expand = True)

    def createAddThema(self,themataKatigorias,index):
        self.themaFrame = tk.Frame(self.frame)

        allThemata = dbUtility.get(self.master.path,("SELECT * FROM Thema",list()))

        self.themaMenu = tk.Menubutton(self.themaFrame, text = "Προσθήκη Θέματος",borderwidth = 5, relief = "groove")
        self.themaMenu.menu = tk.Menu(self.themaMenu)
        self.themaMenu["menu"] = self.themaMenu.menu
        menuItems = self.findNonExisting(allThemata,themataKatigorias,index)
        for val in menuItems:
            l = str(self.master.katigoriaId) + "*" + str(val[0]) + "*" + val[1]
            self.themaMenu.menu.add_radiobutton(label = l, value = l, variable = self.addThema)

        self.themaMenu.pack()
        self.themaFrame.pack(side = "top",fill = "x", expand = True)

    def findNonExisting(self,allList,existList,index):
        for i in existList:
            l = len(allList)
            for j in range(l):
                if int(allList[j][0]) == int(i[index]):
                    allList.pop(j)
                    break
        return allList
