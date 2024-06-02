import tkinter as tk

import dbOrNotdb as dbUtility
import scrollableFrame as scrollableFrame
from tkinter.scrolledtext import ScrolledText
import buttonList as buttonList

class prosthikiHander(tk.Tk):

    def __del__(self):

        print("Ending prosthiki")

    def __init__(self,master):
        self.master = master
        self.master.ntestroy(self)

        self.katigories = listHandler(self,\
        "SELECT * FROM Katigoria where id <> ?",\
        "delete Katigories",\
        "INSERT INTO Katigoria (title) VALUES (?)",\
        None,\
        None,\
        "Update Katigoria set title = ? where id = ?",\
        self.master.mainFrame)
        self.themata = listHandler(self,\
        "select f.id, t.desc from (FramesKatigorias as f left Join Thema as t on t.id = f.themaId) where f.katigoriaId = ?",\
        "delete Themata",\
        "INSERT INTO Thema (desc) VALUES (?)",\
        "select id from Thema where desc = ?",\
        "INSERT INTO FramesKatigorias (katigoriaId,themaId) VALUES (?,?)",\
        "Update Thema set desc = ? where id = ?",\
        self.master.mainFrame)
        self.keimena = listHandler(self,\
        "select b.keimenaId,k.title from (Buttons as b left Join Keimena as k on k.id = b.keimenaId) where b.themaKatigoriasId = ?",\
        "delete Keimena",\
        "INSERT INTO Keimena (title) VALUES (?)",\
        "select id from Keimena where title = ?",\
        "INSERT INTO Buttons (themaKatigoriasId, keimenaId) VALUES (?,?)",\
        "Update Keimena set title = ? where id = ?",\
        self.master.mainFrame)
        self.proboliKeimenou = proboliKeimenou(self,"select desc from Keimena where id = ?","delete proboliKeimenou")



        self.katigories.selectionList.slaveList = self.themata.selectionList
        self.themata.selectionList.slaveList = self.keimena.selectionList
        self.keimena.selectionList.slaveList = self.proboliKeimenou


        self.katigories.selectionList.createButtonList(-1)

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

    def createButtonList(self, id):
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

    def deleteButtonList(self):
        for item in self.frame.winfo_children():
            item.destroy()

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




class listHandler(tk.Tk):
    def __del__(self):
        print(self.delMsg)

    def __init__(self,master,selectAllQuery,delMsg,insertNewEntryQuery,selectNewEntryQuery,insertNewEntryDependancyQuery,updateEntryQuery,mainFrame):
        self.master = master
        self.mainFrame = mainFrame
        self.selectAllQuery = selectAllQuery
        self.insertNewEntryQuery = insertNewEntryQuery
        self.selectNewEntryQuery = selectNewEntryQuery
        self.insertNewEntryDependancyQuery = insertNewEntryDependancyQuery
        self.updateEntryQuery = updateEntryQuery
        self.delMsg = delMsg
        self.slaveList = None

        self.valueSelectedId = tk.StringVar()
        self.valueSelectedId.trace('w', self.idValueChange)

        self.valueSelectedTitle = tk.StringVar()

        self.selectionList = buttonList.buttonList(self,self.selectAllQuery,self.valueSelectedId,self.valueSelectedTitle,"delete ButtonList",self.mainFrame,self.master.master.path)


        self.utilityList = buttonList.utilityButtonList(self,self.valueSelectedId,self.valueSelectedTitle,self.selectionList.frame)


    def createNewButttonForList(self,value):

        dbUtility.add(self.master.master.path,(self.insertNewEntryQuery,(value,)))

        if (self.selectNewEntryQuery != None):
            newEntry = dbUtility.get(self.master.master.path,(self.selectNewEntryQuery,(value,)))[0][0]
            dbUtility.add(self.master.master.path,(self.insertNewEntryDependancyQuery,(self.selectionList.masterValueSelected,newEntry)))

        else:
            pass
        self.selectionList.deleteButtonList()
        self.selectionList.createButtonList(self.selectionList.masterValueSelected)


    def changeButttonFromList(self,value, id):
        dbUtility.add(self.master.master.path,(self.updateEntryQuery,(value,id)))
        self.selectionList.deleteButtonList()
        self.selectionList.createButtonList(self.selectionList.masterValueSelected)


    def idValueChange(self,*args):
        value = self.valueSelectedId.get()
        if value == "+++":
            self.utilityList.changeBut.configure(state = "disabled")
            self.utilityList.delBut.configure(state = "disabled")
        elif "---" in value:
            self.utilityList.addBut.configure(state = "disabled")
            self.utilityList.changeBut.configure(state = "disabled")
        elif "!!!" in value:
            self.utilityList.addBut.configure(state = "disabled")
            self.utilityList.delBut.configure(state = "disabled")
        else:
            try:
                self.utilityList.addBut.configure(state = "normal")
            except:
                pass

            try:
                self.utilityList.changeBut.configure(state = "normal")
            except:
                pass

            try:
                self.utilityList.delBut.configure(state = "normal")
            except:
                pass
