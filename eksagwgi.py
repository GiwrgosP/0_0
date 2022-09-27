import tkinter as tk
from tkinter import tix
import dbOrNotdb as dbUtility


class eksagwgiHander(tk.Tk):

    def __del__(self):
        self.frame.destroy()
        print("Ending Phase_2")

    def __init__(self,master):
        self.master = master
        self.master.ntestroy(self)
        self.frame = tk.Frame(self.master.mainFrame, bg = "#ffffff", borderwidth = 5, relief = "groove")
        self.exportData()
        self.frame.pack(fill = "both", expand = True)


    def listToDict(self, li):
        dict = {}
        for l in li:
            print(l)
            if l[0] in dict.keys():
                pass
            else:
                dict[l[0]] = {}

            if l[1] in dict[l[0]].keys():
                pass
            else:
                dict[l[0]][l[1]] = list()

            dict[l[0]][l[1]].append((l[2],l[3]))

        return dict

    def exportData(self):

        temp = dbUtility.get(self.master.path,("select\
        k.title,\
        t.desc,\
        kei.title, kei.desc\
        from ((Buttons as b \
        left join Keimena kei on b.keimenaId = kei.id\
        left join FramesKatigorias fk on b.themaKatigoriasId = fk.id\
        left join Katigoria k on fk.katigoriaId = k.id) \
        left join Thema t on fk.themaId = t.id)\
        order by k.title asc,t.desc asc;",list()))
        temp = self.listToDict(temp)

        with open(self.master.path +'\export.txt', 'w', encoding="utf-8") as f:
            for t in temp:
                f.write("\n Κατηγορία " + str(t))
                f.write("{")
                for e in temp[t]:
                    f.write("\n Θέμα " + str(e))
                    f.write("[")
                    for m in temp[t][e]:
                        f.write("\n Τίτλος " + str(m[0]))
                        f.write("\n Κείμενο " + str(m[1]))
                        f.write("\n")

                    f.write("]")
                    f.write("\n")

                f.write("}")
                f.write("\n")
