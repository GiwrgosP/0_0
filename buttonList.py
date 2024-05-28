import tkinter as tk

import scrollableFrame as scrollableFrame
import dbOrNotdb as dbUtility

class buttonList(tk.Tk):

    def __del__(self):
        print(self.delMsg)

    def __init__(self,master,query,delMsg):
        self.master = master
        self.query = query
        self.delMsg = delMsg
        self.slaveList = None
        self.but = {}
        self.valueSelected = None


        self.frame = tk.Frame(self.master.master.mainFrame,bg = "#b9b5b5", borderwidth = 5, relief = "groove")
        self.frame.pack(side = "left", fill = "y", anchor = "nw")

    def createButtonList(self, id):

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
        if self.valueSelected != None:
            self.but[self.valueSelected].configure(state = "normal")

        self.but[id].configure(state = "disabled")

        self.valueSelected = id

        self.slaveList.deleteButtonList()
        self.slaveList.createButtonList(id)

    def deleteButtonList(self):
        for item in self.frame.winfo_children():
            item.destroy()
        self.slaveList.deleteButtonList()
        self.but.clear()
        self.valueSelected = None
