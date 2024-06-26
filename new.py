import tkinter as tk
from tkinter import tix
from tkinter.messagebox import askyesno
import dbOrNotdb as dbUtility
import scrollableFrame as scrollableFrame
from tkinter.scrolledtext import ScrolledText

class newHander(tk.Tk):

    def __del__(self):

        print("Ending prosthiki")

    def __init__(self,master):
        self.master = master
        self.master.ntestroy(self)
        self.tip = tix.Balloon(self.master.window)

        self.katigories = buttonList(self,\
        "SELECT * FROM Katigoria where id <> ?",\
        "delete Katigories")
        self.themata = buttonList(self,\
        "select f.id, t.desc from (FramesKatigorias as f left Join Thema as t on t.id = f.themaId) where f.katigoriaId = ?",\
        "delete Themata")
        self.keimena = buttonList(self,"select b.keimenaId,k.title from (Buttons as b left Join Keimena as k on k.id = b.keimenaId) where b.themaKatigoriasId = ?","delete Keimena")
        self.proboliKeimenou = proboliKeimenou(self,"select desc from Keimena where id = ?","delete proboliKeimenou")



        self.katigories.slaveList = self.themata
        self.themata.slaveList = self.keimena
        self.keimena.slaveList = self.proboliKeimenou


        self.katigories.createBut(-1)

    def createNewButttonForList(self,buttonList,value):

        if buttonList == self.katigories:

            query = "INSERT INTO Katigoria (title) VALUES (?)"
            dbUtility.add(self.master.path,(query,(value,)))

        elif buttonList == self.themata:

            query = "INSERT INTO Thema (desc) VALUES (?)"
            dbUtility.add(self.master.path,(query,(value,)))

            themaId = dbUtility.get(self.master.path,("select id from Thema where desc = ?",(value,)))[0][0]

            query = "INSERT INTO FramesKatigorias (katigoriaId,themaId) VALUES (?,?)"
            dbUtility.add(self.master.path,(query,(buttonList.createId,themaId)))

        elif buttonList == self.keimena:

            query = "INSERT INTO Keimena (title) VALUES (?)"
            dbUtility.add(self.master.path,(query,(value,)))

            keimenoId = dbUtility.get(self.master.path,("select id from Keimena where title = ?",(value,)))[0][0]

            query = "INSERT INTO Buttons (themaKatigoriasId, keimenaId) VALUES (?,?)"
            dbUtility.add(self.master.path,(query,(buttonList.createId,keimenoId)))

        elif buttonList == self.proboliKeimenou:
            pass
        else:
            pass

        buttonList.createBut(buttonList.createId)


class proboliKeimenou(tk.Tk):

    def __del__(self):
        print(self.delMsg)

    def __init__(self,master,query, delMsg):
        self.master = master
        self.query = query
        self.delMsg = delMsg
        self.createId = None
        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#ffffff", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "both", expand = True, anchor = "nw")

    def createBut(self, id):
        self.createId = id
        self.saveBut = tk.Button(self.frame, text = "Αποθήκευση", command = lambda: self.saveButFunction(),  justify = "left", borderwidth = 5, relief = "groove")
        self.saveBut.pack(side = "top")
        self.keimenoText = ScrolledText(self.frame)
        keimena =self.getChoiceValues(id)
        if keimena != None:
            self.keimenoText.insert(tk.END, keimena)
        else:
            pass
        self.keimenoText.pack(fill = "both",expand = True)

    def getChoiceValues(self,id):
        return  dbUtility.get(self.master.master.path,(self.query,(id,)))[0][0]

    def saveButFunction(self):
        if self.createId:
            query = "update Keimena set desc = ? where id = ?"
            value = self.keimenoText.get("1.0", tk.END)
            if value.replace(" ", "") != "":
                dbUtility.add(self.master.master.path,(query,(value,self.createId)))
            else:
                pass
        else:
            print("get help")

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
        self.idValue = tk.StringVar()
        self.titleValue = tk.StringVar()
        self.createId = None
        self.idValue.trace('w', self.idValueChange)

        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#b9b5b5", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "y", anchor = "nw")

    def idValueChange(self,*args):
        value = self.idValue.get()
        if value == "+++":
            self.changeBut.configure(state = "disabled")
        #    self.delBut.configure(state = "disabled")
        elif "---" in value:
            self.addBut.configure(state = "disabled")
        #    self.changeBut.configure(state = "disabled")
        elif "!!!" in value:
            self.addBut.configure(state = "disabled")
        #    self.delBut.configure(state = "disabled")
        else:
            try:
                self.addBut.configure(state = "normal")
            except:
                pass


    def createBut(self, id):
        self.createId = id
        self.idLabel = tk.Label(self.frame, textvariable = self.idValue )
        self.titleEntry = tk.Entry(self.frame, textvariable = self.titleValue,width = 25,  justify = "left", borderwidth = 5, relief = "groove")
        self.addBut = tk.Button(self.frame, text = "Προσθήκη Νέου", command = lambda: self.addButFunction(),  justify = "left", borderwidth = 5, relief = "groove")

        self.idLabel.pack(side = "top")
        self.titleEntry.pack(side = "top", fill = "x")
        self.addBut.pack(side = "top", fill = "x")

        self.scrolledFrame = scrollableFrame.VerticalScrolledFrame(self.frame)
        self.scrolledFrame.configure(borderwidth = 8, relief = "groove")
        self.scrolledFrame.pack(expand = False)

        self.scrolledFrame2 = scrollableFrame.VerticalScrolledFrame(self.frame)
        self.scrolledFrame2.configure(borderwidth = 8, relief = "groove")
        self.scrolledFrame2.pack(expand = False)

        butList = self.getChoiceValues(id)

        for widget in butList:
            id,title = widget
            slaveList = self.slaveList.getChoiceValues(id)
            if slaveList:
                but = tk.Button(self.scrolledFrame.interior, width = 20, wraplength = 100,  justify = "left", text = title, command = lambda x = id, y = title : self.butFunction(x,y), relief = "groove")
                but.pack(side = "top", fill = "x")
            else:
                but = tk.Button(self.scrolledFrame2.interior, width = 20, wraplength = 100,  justify = "left", text = title, command = lambda x = id, y = title : self.butFunction(x,y), relief = "groove")
                but.pack(side = "top", fill = "x")

            self.but[id] = but

    def butFunction(self,id,title):
        if self.value != None:
            self.but[self.value].configure(state = "normal")

        self.but[id].configure(state = "disabled")

        self.value = id
        self.idValue.set(str(id))
        self.titleValue.set(title)

        self.slaveList.createBut(id)


    def addButFunction(self):
        idValue = self.idValue.get()
        value = self.titleValue.get()
        if idValue == "+++":
            answer = askyesno(title='Θες;', message='Προσθήκη νέου με Τίτλο ' + value)
            if answer:
                if value.replace(" ", "") != "":
                    self.master.createNewButttonForList(self, value)
                else:
                    pass
            else:
                pass
        else:
            self.idValue.set("+++")

    def getChoiceValues(self,id):
        return dbUtility.get(self.master.master.path,(self.query,(id,)))
