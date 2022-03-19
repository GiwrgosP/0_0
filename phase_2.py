import tkinter as tk
from operator import itemgetter
import pyperclip
import dbOrNotdb as dbUtility

class windowHander(tk.Tk):

    def __del__(self):
        self.item1.__del__()
        print("Ending Phase_2")

    class katigoria():
        def __del__(self):
            print("END katigoria")

        def updateCallback(self):

            id = self.values["id"].get()
            desc = self.values["desc"].get()
            if desc != "+++":
                if id == "+++":
                    dbUtility.add(self.master.master.path,("INSERT INTO Katigoria (title) VALUES (?)",(desc,)))
                else:
                    dbUtility.add(self.master.master.path,("UPDATE Katigoria SET title = ? WHERE id = ?", (desc,id)))
                self.master.master.createKatigoriaSection()
            else:
                pass



        def descCallBack(self, *args):
            variableValue = self.values["desc"].get()

            index = self.master.getIndexFormList(variableValue,self.menuValues["desc"])
            if index != -1:
                self.values["id"].set(self.menuValues["id"][index])
                self.updateButton.configure(state = "disabled")
            else:
                self.updateButton.configure(state = "normal")
                if variableValue == "+++":
                    self.values["id"].set("+++")

            idValue = self.values["id"].get()

            if idValue == "+++":
                self.updateButton.configure(text = "Προσθήκη περιγραφής")
            else:
                self.updateButton.configure(text = "Αλλαγή περιγραφής")

        def __init__(self,master):
            self.master = master
            self.values = { \
            "id" :  tk.StringVar(),\
            "desc" : tk.StringVar()}

            self.menuValues = { \
            "id" :  list(),\
            "desc" : list()}

            frame = tk.Frame(self.master.frame,borderwidth = 3, relief = "groove")

            label = tk.Label(frame, text = "Κατηγορία")
            label.pack(side = "left",padx=2, pady=2)

            temp = dbUtility.get(self.master.master.path,("SELECT * FROM Katigoria",list()))
            for kat in temp:
                id, desc = kat
                self.menuValues["id"].append(id)
                self.menuValues["desc"].append(desc)

            menu = tk.Menubutton(frame, text = "Επιλογές Κατηγορίας",borderwidth = 3, relief = "groove")
            self.master.fillMenuWithValues(menu, self.menuValues["desc"], self.values["desc"])
            menu.pack(side = "left",padx=2, pady=2)

            label2 = tk.Label(frame, textvariable = self.values["id"])
            label2.pack(side = "left",padx=2, pady=2)
            entry =  tk.Entry(frame, textvariable = self.values["desc"], width = 50)
            entry.pack(side = "left",padx=2, pady=2)
            self.updateButton = tk.Button(frame, text = "Αλλαγή περιγραφής", state = "disabled", command = lambda : self.updateCallback())
            self.updateButton.pack(side = "right")
            frame.pack(side = "top", fill = "x", expand = True)

            traceDesc = self.values["desc"].trace_add('write', self.descCallBack)


    class thema():

        def updateCallback(self):
            id = self.values["id"].get()
            desc = self.values["desc"].get()
            color = self.values["color"].get()

            try:
                self.colorFrame.configure(bg = color)
            except:
                color = None

            if desc != "+++":
                if id == "+++":
                    dbUtility.add(self.master.master.path,("INSERT INTO Thema (desc,colorCode) VALUES (?,?)",(desc,color)))
                else:
                    indexDesc = self.master.getIndexFormList(desc,self.menuValues["desc"])

                    if color == None:
                        if indexDesc == -1:
                            dbUtility.add(self.master.master.path,("UPDATE Thema SET desc = ? WHERE id = ?", (desc,id)))
                    else:
                        colorAtIndex = self.menuValues["desc"][indexDesc]
                        if colorAtIndex != color:
                            dbUtility.add(self.master.master.path,("UPDATE Thema SET colorCode = ? WHERE id = ?", (color,id)))
                        else:
                            pass

                self.master.master.createKatigoriaSection()
            else:
                pass

        def descCallBack(self, *args):
            variableValue = self.values["desc"].get()

            index = self.master.getIndexFormList(variableValue,self.menuValues["desc"])

            if index != -1:
                self.values["id"].set(self.menuValues["id"][index])
                self.values["color"].set(self.menuValues["color"][index])
                self.updateButton.configure(state = "disabled")
            else:
                self.updateButton.configure(state = "normal")
                if variableValue == "+++":
                    self.values["id"].set("+++")

            idValue = self.values["id"].get()
            if idValue == "+++":
                self.updateButton.configure(text = "Προσθήκη περιγραφής")
            else:
                self.updateButton.configure(text = "Αλλαγή περιγραφής")


        def colorCallBack(self, *args):
            color = self.values["color"].get()
            id = self.values["id"].get()
            try:
                self.colorFrame.configure(bg = color)
                if id != "+++":
                    self.updateButton.configure(text = "Αλλαγή περιγραφής")
                    self.updateButton.configure(state = "normal")
            except:
                print("Error Hex Color")

        def __del__(self):
            print("END thema")

        def __init__(self,master):
            self.master = master
            self.values = { \
            "id" :  tk.StringVar(),\
            "desc" : tk.StringVar(),\
            "color" : tk.StringVar()}

            self.menuValues = { \
            "id" :  list(),\
            "desc" : list(),\
            "color" : list()}

            frame = tk.Frame(self.master.frame,borderwidth = 3, relief = "groove")

            label = tk.Label(frame, text = "Θέμα")
            label.pack(side = "left")

            temp = dbUtility.get(self.master.master.path,("SELECT * FROM Thema",list()))

            for them in temp:
                id, desc, color = them
                self.menuValues["id"].append(id)
                self.menuValues["desc"].append(desc)
                self.menuValues["color"].append(color)

            menu = tk.Menubutton(frame, text = "Επιλογές Θέματος",borderwidth = 3, relief = "groove")
            self.master.fillMenuWithValues(menu, self.menuValues["desc"], self.values["desc"])
            menu.pack(side = "left")
            label2 = tk.Label(frame, textvariable = self.values["id"])
            label2.pack(side = "left",padx=2, pady=2)
            entry = tk.Entry(frame, textvariable = self.values["desc"], width = 50)
            entry.pack(side = "left")


            self.colorFrame = tk.Frame(frame, height = 35, width = 35, borderwidth = 2, relief = "groove")
            self.colorFrame.pack(side = "left",padx=2, pady=2)
            colorEntry = tk.Entry(frame, textvariable = self.values["color"])
            colorEntry.pack(side = "left")
            self.updateButton = tk.Button(frame, text = "Αλλαγή θέματος", state = "disabled", command = lambda : self.updateCallback())
            self.updateButton.pack(side = "right")

            frame.pack(side = "top", fill = "x", expand = True)

            traceDesc = self.values["desc"].trace_add('write', self.descCallBack)
            traceColor = self.values["color"].trace_add('write', self.colorCallBack)

    class keimeno():

        def titleCallBack(self, *args):
            variableValue = self.values["title"].get()
            index = self.master.getIndexFormList(variableValue,self.menuValues["title"])
            if index != -1:
                self.values["id"].set(self.menuValues["id"][index])
                self.values["desc"].set(self.menuValues["desc"][index])
                self.entryDesc.delete("1.0",tk.END)
                self.entryDesc.insert(tk.END,self.menuValues["desc"][index])
                self.updateButton.configure(state = "disabled")
            else:
                self.updateButton.configure(state = "normal")
                if variableValue == "+++":
                    self.values["id"].set("+++")

                idValue = self.values["id"].get()
                if idValue == "+++":
                    self.updateButton.configure(text = "Προσθήκη περιγραφής")
                else:
                    self.updateButton.configure(text = "Αλλαγή περιγραφής")


        def __del__(self):
            print("END keimeno")

        def updateCallback(self):
            id = self.values["id"].get()
            title = self.values["title"].get()


            if title != "+++":
                desc = self.entryDesc.get("1.0",tk.END)
                if id == "+++":
                    dbUtility.add(self.master.master.path,("INSERT INTO Keimena (title,desc) VALUES (?,?)",(title,desc)))
                else:
                    indexDesc = self.master.getIndexFormList(desc,self.menuValues["desc"])
                    indexTitle = self.master.getIndexFormList(title,self.menuValues["title"])
                    if indexDesc == -1:
                        dbUtility.add(self.master.master.path,("UPDATE Keimena SET desc = ? WHERE id = ?", (desc,id)))
                    if indexTitle == -1:
                        dbUtility.add(self.master.master.path,("UPDATE Keimena SET title = ? WHERE id = ?", (title,id)))

                self.master.master.createKatigoriaSection()
            else:
                pass

        def __init__(self,master):
            self.master = master
            self.values = { \
            "id" :  tk.StringVar(),\
            "title" :  tk.StringVar(),\
            "desc" : tk.StringVar()}

            self.menuValues = { \
            "id" :  list(),\
            "title" :  list(),\
            "desc" : list()}

            frame = tk.Frame(self.master.frame,borderwidth = 3, relief = "groove")
            utilityFrame = tk.Frame(frame, borderwidth = 3, relief = "groove")
            descFrame = tk.Frame(frame, borderwidth = 3, relief = "groove")

            label = tk.Label(utilityFrame, text = "Κείμενο")
            label.pack(side = "left")

            temp = dbUtility.get(self.master.master.path,("SELECT * FROM Keimena",list()))
            for keim in temp:
                id, title, desc = keim
                self.menuValues["id"].append(id)
                self.menuValues["title"].append(title)
                self.menuValues["desc"].append(desc)


            menu = tk.Menubutton(utilityFrame, text = "Επιλογές Κειμένου",borderwidth = 3, relief = "groove")
            self.master.fillMenuWithValues(menu, self.menuValues["title"], self.values["title"])
            menu.pack(side = "left")
            label2 = tk.Label(utilityFrame, textvariable = self.values["id"])
            label2.pack(side = "left",padx=2, pady=2)
            entry = tk.Entry(utilityFrame, textvariable = self.values["title"], width = 50)
            entry.pack(side = "left")
            self.updateButton = tk.Button(utilityFrame, text = "Αλλαγή θέματος", state = "disabled", command = lambda : self.updateCallback())
            self.updateButton.pack(side = "right")


            self.entryDesc =  tk.Text(descFrame, width = 100)
            self.entryDesc.insert(tk.END,self.values["desc"].get())
            self.entryDesc.pack(side = "top",fill = "both", expand = True)

            utilityFrame.pack(side = "top",fill = "both", expand = True)
            descFrame.pack(side = "top",fill = "both", expand = True)
            frame.pack(side = "top",fill = "both", expand = True)

            traceTitle= self.values["title"].trace_add('write', self.titleCallBack)

    def __init__(self,master):

        self.master = master
        self.frame = tk.Frame(self.master.mainFrame,borderwidth = 5, relief = "groove")
        self.item1 = self.katigoria(self)
        self.item2 = self.thema(self)
        self.item3 = self.keimeno(self)
        self.frame.grid(column = 0, row = 1, sticky = "ewsn",columnspan = 2)


    def fillMenuWithValues(self,menuObj,values,variable):
        menuObj.menu = tk.Menu(menuObj)
        menuObj["menu"] = menuObj.menu
        menuObj.menu.add_radiobutton(label = "+++", value = "+++", variable = variable)
        for val in values:
            menuObj.menu.add_radiobutton(label = val, value = val, variable = variable)


    def getIndexFormList(self,value,valueList):
        index = 0
        for val in valueList:
            if val == value:
                return index
            index += 1
        return -1
