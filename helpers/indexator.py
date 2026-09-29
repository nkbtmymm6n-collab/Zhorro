import sqlite3
import pymupdf
from docx import Document

def indexator(paths):

    db=sqlite3.connect("zhorro.db")

    for path in paths:
        words=[]
        suffix=path.suffix.lower()
        file_id=db.execute("SELECT id FROM files WHERE path=?",(str(path),)).fetchone()[0]
        

        if suffix==".txt":
        
            with open(path, "r", encoding="utf-8") as file:
                text=file.read()
                words.extend(text.split())
            file.close()

        elif suffix==".pdf":

            doc = pymupdf.open(path)

            for page in doc:
                text=page.get_text()
                words.extend(text.split())
                

            doc.close()

        elif suffix==".docx":

            doc=Document(path)

            for paragraph in doc.paragraphs:
                text=paragraph.text
                words.extend(text.split())
        print("WORDS LENGTH:", len(words))
        for word in words:
            word=word.lower()
            db.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word,))
            word_id=db.execute("SELECT id FROM words WHERE word = ?", (word,)).fetchone()[0]
            db.execute("INSERT OR IGNORE INTO word_files (word_id, file_id) VALUES (?, ?)", (word_id, file_id))

    db.commit()
    db.close()
            

        
        
