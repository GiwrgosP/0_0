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

        # Filter out stop words and non-alphabetic tokens
        filtered_tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
        filtered_desc = " ".join(filtered_tokens)

        # Recreate the doc with filtered description
        filtered_doc = nlp(filtered_desc)

        vector = filtered_doc.vector.tobytes()  # Convert the vector to bytes for storage

        dbUtility.add(path, ("INSERT INTO nlp (title, desc, vector) VALUES (?, ?, ?)", (title, filtered_desc, vector)))

if __name__ == "__main__":
    main()
