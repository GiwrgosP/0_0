import tkinter as tk
from tkinter import messagebox
import dbOrNotdb as dbUtility
import spacy
import numpy as np
import os

# Load spaCy model
nlp = spacy.load('el_core_news_sm')

def search_texts():
    keyword = search_entry.get()
    if not keyword:
        messagebox.showwarning("Input Error", "Please enter a keyword to search.")
        return

    path = os.path.dirname(os.path.abspath(__file__))
    results = dbUtility.get(path,("SELECT title,desc,vector FROM nlp WHERE id <> ?",(-1,)))


    similarities = []
    for result in results:
        text_vector = np.frombuffer(result[3], dtype=np.float32)
        similarity = np.dot(keyword_vector, text_vector) / (np.linalg.norm(keyword_vector) * np.linalg.norm(text_vector))
        similarities.append((similarity, result))

    # Sort results by similarity in descending order
    similarities.sort(reverse=True, key=lambda x: x[0])

    # Update the listbox with top results
    for similarity, result in similarities[:10]:  # Show top 10 results
        result_listbox.insert(tk.END, f"Category: {result[0]}, Subcategory: {result[1]}, Text: {result[2]}")


# Create the main window
root = tk.Tk()
root.title("Text Search Application")

# Create and place the search bar
search_label = tk.Label(root, text="Enter keyword:")
search_label.pack(pady=5)
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

# Create and place the search button
search_button = tk.Button(root, text="Search", command=search_texts)
search_button.pack(pady=5)

# Create and place the listbox to display results
result_listbox = tk.Listbox(root, width=100, height=20)
result_listbox.pack(pady=10)

# Run the main loop
root.mainloop()
