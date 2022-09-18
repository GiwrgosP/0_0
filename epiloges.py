import tkinter as tk
from tkinter import tix
import pyperclip
import dbOrNotdb as dbUtility


class epilogesHander(tk.Tk):

    def __del__(self):
       print("Ending Phase_1")

    def __init__(self,master):
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
             but = tk.Button(self.frameKatigories, text = title, command = lambda x = id : self.createKeimenaFrame(x))
             but.grid(column  = 0, row = row)
             row += 1
             
        self.frameKatigories.grid( column  = 0, row = 0, sticky = "ewns")
        
        
    def createKeimenaFrame(self,id):
        try:
            self.keimenaFrame.destroy()
        except: 
            pass    
        
        self.keimenaFrame= tk.Frame(self.master.mainFrame, bg = "#ffffff", borderwidth = 5, relief = "groove")
        themataList = dbUtility.get(self.master.path,("SELECT id,themaId FROM FramesKatigorias WHERE katigoriaId = ?", (id,)))
        
        for thema in themataList:
            themaKatigoriaId,  themaId = thema
            themaTitle, themaColor = dbUtility.get(self.master.path,("SELECT desc,colorCode FROM Thema WHERE id = ?",(themaId,)))[0]
            themaFrame = tk.Frame(self.keimenaFrame, bg = themaColor, borderwidth = 3, relief = "groove")
            label = tk.Label(themaFrame, text = themaTitle )
            label.pack(side = "left",padx=2, pady=2)
            
            keimenaThematosKatigorias = dbUtility.get(self.master.path,("SELECT id,keimenaId FROM Buttons WHERE themaKatigoriasId = ?",(themaKatigoriaId,)))
            
            for keimeno in keimenaThematosKatigorias:
                garbage, keimenoId =  keimeno
                title, keimeno = dbUtility.get(self.master.path,("SELECT title,desc FROM Keimena WHERE id = ?",(keimenoId,)))[0]
                but = (tk.Button(themaFrame, text = title, command = lambda x = keimeno : pyperclip.copy(x) ))
                but.pack(padx=2, pady=2)
                
      
        
            themaFrame.pack(fill = "x",  expand = True)
        
        
        self.keimenaFrame.grid( column  = 1, row = 0, sticky = "ewns")