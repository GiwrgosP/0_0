import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import dbOrNotdb as dbUtility

class anazitisiHander(tk.Tk):
    def __init__(self):
        super().__init__()

        # Database connection
        self.con = dbUtility.connect()  # Assuming dbUtility.connect() returns a connection object

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

    def create_search_tab(self):
        # Search Entry
        tk.Label(self.grid(row=0, column=0, padx=15, pady=15, sticky='w')
        search_entry = tk.Entry(textvariable=self.search_text_var)
        search_entry.grid(row=0, column=1, padx=15, pady=15, sticky='ew')

        # Search Button
        buttonSearch = tk.Button(tab, text="Search", command=self.search_records)
        buttonSearch.grid(row=0, column=2, padx=15, pady=15, sticky='w')

        # Results Text Widget
        self.results_text = ScrolledText(tab, wrap=tk.WORD)
        self.results_text.grid(row=1, column=0, columnspan=3, padx=15, pady=15, sticky='nsew')

        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(1, weight=1)

    def search_records(self):
        sql_query = "SELECT * FROM bd WHERE Family_Name=%s"
        vals = (self.search_text_var.get(), self.search_text_var.get())

        cursor = self.con.cursor()
        cursor.execute(sql_query, vals)

        my_rows = cursor.fetchall()
        total_rows = cursor.rowcount

        cursor.close()

        self.display_results(my_rows, total_rows)

    def display_results(self, rows, total_rows):
        self.results_text.delete(1.0, tk.END)  # Clear previous results
        if total_rows == 0:
            self.results_text.insert(tk.END, "No records found.")
        else:
            for row in rows:
                self.results_text.insert(tk.END, f"{row}\n")
            self.results_text.insert(tk.END, f"\nTOTAL ROWS: {total_rows}")

    def on_closing(self):
        if self.con:
            self.con.close()
        self.destroy()

if __name__ == "__main__":
    app = anazitisiHander()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
