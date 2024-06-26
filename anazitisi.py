import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import dbOrNotdb as dbUtility
import os
class anazitisiHander(tk.Tk):
    def __init__(self):
        super().__init__()
        self.path = os.path.dirname(os.path.abspath(__file__))
        # Database connection
        self.con = dbUtility.conn(self.path)  # Assuming dbUtility.connect() returns a connection object

        # Variables
        self.search_text_var = tk.StringVar()

        # Create notebook tabs
        self.create_notebook_tabs()

    def create_notebook_tabs(self):
        tab_parent = ttk.Notebook(self)

        tab3 = ttk.Frame(tab_parent)

        tab_parent.add(tab3, text="Search")

        tab_parent.pack(expand=1, fill='both')

        # Add widgets to the search tab
        self.create_search_tab(tab3)

    def create_search_tab(self,tab):
        # Search Entry
        search_label = tk.Label()
        search_label.pack()
        search_entry = tk.Entry(textvariable=self.search_text_var)
        search_entry.pack()

        # Search Button
        buttonSearch = tk.Button(tab, text="Search", command=self.search_records)
        buttonSearch.pack()

        # Results Text Widget
        self.results_text = ScrolledText(tab, wrap=tk.WORD)
        self.results_text.pack()


    def search_records(self):
        sql_query = "SELECT * FROM Keimena WHERE desc=?"
        vals = self.search_text_var.get()

        result = dbUtility.get(self.path, (sql_query,(vals,)))


        self.display_results(result)

    def display_results(self, total_rows):
        self.results_text.delete(1.0, tk.END)  # Clear previous results
        if total_rows == 0:
            self.results_text.insert(tk.END, "No records found.")
        else:
            self.results_text.insert(tk.END, f"\nTOTAL ROWS: {total_rows}")

    def on_closing(self):
        if self.con:
            self.con.close()
        self.destroy()

if __name__ == "__main__":
    app = anazitisiHander()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
