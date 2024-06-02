import tkinter as tk
import scrollableFrame as scrollableFrame
import dbOrNotdb as dbUtility
from tkinter.messagebox import askyesno

class buttonList(tk.Tk):

    def __del__(self):
        print(self.delMsg)

    def __init__(self,master,query,idValue,idTitle,delMsg,mainFrame,path):
        self.master = master
        self.mainFrame = mainFrame
        self.path = path
        self.query = query
        self.delMsg = delMsg
        self.slaveList = None
        self.masterValueSelected = None
        self.but = {}
        self.valueSelected = idValue
        self.titleSelected = idTitle

        self.frame = tk.Frame(self.mainFrame,bg = "#b9b5b5", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "y", anchor = "nw")

    def createButtonList(self, id):
        self.masterValueSelected = id

        self.scrolledFrame = scrollableFrame.VerticalScrolledFrame(self.frame)
        self.scrolledFrame2 = scrollableFrame.VerticalScrolledFrame(self.frame)

        self.scrolledFrame.configure(borderwidth = 5, relief = "groove")
        self.scrolledFrame.pack(fill = "y", expand =True)

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
        value = self.valueSelected.get()

        if value != "":
            self.but[int(value)].configure(state = "normal")

        self.but[id].configure(state = "disabled")

        self.valueSelected.set(str(id))
        self.titleSelected.set(title)


        self.slaveList.deleteButtonList()
        self.slaveList.createButtonList(id)

    def deleteButtonList(self):
        try:
            for item in self.scrolledFrame.winfo_children():
                item.destroy()
            self.scrolledFrame.destroy()
            for item in self.scrolledFrame2.winfo_children():
                item.destroy()
            self.scrolledFrame2.destroy()
        except:
            pass
        self.slaveList.deleteButtonList()
        self.but.clear()
        self.valueSelected.set("")

    def getChoiceValues(self,id):
        return dbUtility.get(self.path,(self.query,(id,)))


class utilityButtonList(tk.Tk):
    def __init__(self,master, idValue, idTitle,frame):
        self.master = master
        self.valueSelected = idValue
        self.titleSelected = idTitle

        self.frame = frame

        self.idLabel = tk.Label(self.frame, textvariable = self.valueSelected )
        self.titleEntry = tk.Entry(self.frame, textvariable = self.titleSelected,width = 25,  justify = "left", borderwidth = 5, relief = "groove")
        self.addBut = tk.Button(self.frame, text = "Προσθήκη Νέου", command = lambda: self.addButFunction(),  justify = "left", borderwidth = 5, relief = "groove")
        self.changeBut = tk.Button(self.frame, text = "Αλλαγή Επιλεγμένου", command = lambda: self.changButFunction(), justify = "left", borderwidth = 5, relief = "groove")
        self.delBut = tk.Button(self.frame, text = "Διαγραφή Επιλεγμένου",  command = lambda: self.deleteButFunction(), justify = "left", borderwidth = 5, relief = "groove")

        self.changeBut.configure(state = "disabled")
        self.delBut.configure(state = "disabled")

        self.idLabel.pack(side = "top")
        self.titleEntry.pack(side = "top", fill = "x")
        self.addBut.pack(side = "top", fill = "x")
        self.changeBut.pack(side = "top", fill = "x")
        self.delBut.pack(side = "top", fill = "x")

#ayti i malakia den kanei update gia ta themata einai lathos to query gia tin epilogi thematwn me basi tin katigoria epilogis kai epistrefei lathos id gia thema
    def changButFunction(self):
        idValue = self.valueSelected.get()
        value = self.titleSelected.get()
        if "!!!" in idValue:
            answer = askyesno(title='Θες;', message="Αλλαγή  σε " + value)
            if answer and value != "":
                self.master.changeButttonFromList(value, idValue[:-3])
            else:
                pass
        else:
            str = idValue + "!!!"
            self.valueSelected.set(str)


#Auti i malakia den kanei diagrafi, sto true tou answer kanei pass
    def deleteButFunction(self):
        idValue = self.valueSelected.get()
        value = self.titleSelected.get()
        if "---" in idValue:
            answer = askyesno(title='Θες;', message='Διαγραφή ' + value)
            if answer:
                pass
            else:
                pass
        else:
            str = idValue + "---"
            self.valueSelected.set(str)

    def addButFunction(self):
        idValue = self.valueSelected.get()
        value = self.titleSelected.get()
        if idValue == "+++":
            answer = askyesno(title='Θες;', message='Προσθήκη νέου με Τίτλο ' + value)
            if answer:
                if value.replace(" ", "") != "":
                    self.master.createNewButttonForList(value)
                else:
                    pass
            else:
                pass
        else:
            self.valueSelected.set("+++")
