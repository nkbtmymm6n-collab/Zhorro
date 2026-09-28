from pathlib import Path
from docx import Document
from sentence_transformers import SentenceTransformer
from .appender import appender
import pymupdf
import sqlite3

def finder(word):
    model=SentenceTransformer("all-MiniLM-L6-v2")
    word=word.lower()
    db=sqlite3.connect("zhorro.db")
    files=(db.execute("SELECT files.path FROM files JOIN word_files ON word_files.file_id=files.id JOIN words ON word_files.word_id=words.id WHERE words.word=?", (word,))).fetchall()
    list_of_founds=[]
    for file in files:
        path=Path(file[0])
        filename=path.name
        founds={}
        founds["path"]=path
        founds["filename"]=filename
        founds["contexts"]=[]
        list_of_founds.append(founds)

    for file in list_of_founds:
        if Path(file["path"]).suffix==".txt":
            with open (file["path"], "r", encoding="utf-8") as f:
                text=f.read()
                appender(text, file, word, None, model)

        elif Path(file["path"]).suffix==".pdf":
            doc=pymupdf.open(file["path"])
            number=1
            for page in doc:
                text=page.get_text()
                appender(text, file, word, number, model)
                number+=1

        elif Path(file["path"]).suffix==".docx":
            doc=Document(file["path"])
            paragraphs=doc.paragraphs
            number=1
            for paragraph in paragraphs:
                text=paragraph.text
                appender(text, file, word, number, model)
                number+=1       
            
    db.close()
    return list_of_founds

