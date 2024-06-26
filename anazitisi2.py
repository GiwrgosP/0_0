import tkinter as tk
from tkinter import tix
import pyperclip
import dbOrNotdb as dbUtility
import scrollableFrame as scrollableFrame
from tkinter.scrolledtext import ScrolledText


class anazitisiHander(tk.Tk):

def search_records():
    sql_query = "SELECT * FROM bd WHERE Job_Title=%s AND Family_Name=%s"
    vals = (options_var.get(), search_text_var.get())

    cursor = con.cursor()
    cursor.execute(sql_query, vals)

    my_rows = cursor.fetchall()
    total_rows = cursor.rowcount


    cursor.close()
    con.close()

    print(my_rows)
    print("TOTAL ROWS: ", total_rows)
