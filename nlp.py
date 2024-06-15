import os
import spacy
from spacy.lang.el.examples import sentences


import dbOrNotdb as dbUtility


def main():
    nlp = spacy.load("el_core_news_sm")
    path = os.path.dirname(os.path.abspath(__file__))
    texts = dbUtility.get(path,("SELECT title,desc FROM Keimena WHERE id <> ?",(-1,)))


    for title, desc in texts:
        doc = nlp(desc)
        vector = doc.vector.tobytes()  # Convert the vector to bytes for storage

        dbUtility.add(path,("INSERT INTO nlp (title,desc,vector) VALUES (?,?,?)", (title,desc,vector,)))

        print(title)






main()
