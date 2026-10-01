import sqlite3
from pathlib import Path
from docx import Document
from sentence_transformers import SentenceTransformer
from .appender import appender
import pymupdf

def finder(word):
    db=sqlite3.connect("zhorro.db")
    model=SentenceTransformer("all-MiniLM-L6-v2")
    list_of_founds=[]
    list_of_results=[]

    if len(word.split())==1:
        print("WORDS COUNT:", db.execute("SELECT COUNT(*) FROM words").fetchone())
        print("SAMPLE WORDS:", db.execute("SELECT word FROM words LIMIT 20").fetchall())
        word=word.lower()
        files=(db.execute("SELECT files.path FROM files JOIN word_files ON word_files.file_id=files.id JOIN words ON word_files.word_id=words.id WHERE words.word=?", (word,))).fetchall()
        print("WORD ROW:", db.execute(
    "SELECT * FROM words WHERE word=?",
    (word,)
).fetchone())
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
                    None, list_of_results.extend(appender(text, file, word, None, model, True))

            elif Path(file["path"]).suffix==".pdf":
                doc=pymupdf.open(file["path"])
                positions=[]
                number=0
                counter=""
                text=""
                for page in doc:
                    text+=page.get_text()
                    positions.append({"start": len(counter), "end": len(text), "page": number})
                    counter=text
                    number+=1
                    
                None, list_of_results.extend(appender(text, file, word, positions, model, True))

            elif Path(file["path"]).suffix==".docx":
                doc=Document(file["path"])
                paragraphs=doc.paragraphs
                positions=[]
                number=0
                counter=""
                text=""

                for paragraph in paragraphs:
                    text+=paragraph.text
                    positions.append({"start": len(counter), "end": len(text), "paragraph": number})
                    counter=text
                    number+=1
                print("BEFORE APPENDER")
                None, list_of_results.extend(appender(text, file, word, positions, model, True))                
                print("AFTER APPENDER")
                print(file["contexts"])

    elif len(word.split())>1:
        all_files = db.execute("SELECT path FROM files").fetchall()
        for file in all_files:
            path=Path(file[0])
            filename=path.name
            results={}
            results["path"]=path
            results["filename"]=filename

            if results["path"].suffix==".txt":
                with open (results["path"], "r", encoding="utf-8") as f:
                    text=f.read()
                    list_of_results.extend(appender(text, results, word, None, model, False))

            elif results["path"].suffix==".pdf":
                doc=pymupdf.open(results["path"])
                positions=[]
                counter=""
                text=""               
                number=0

                for page in doc:
                    text+=page.get_text()
                    positions.append({"start": len(counter), "end": len(text), "page": number})
                    counter=text
                    number+=1
                
                list_of_results.extend(appender(text, results, word, positions, model, False))

            elif results["path"].suffix==".docx":
                doc=Document(results["path"])
                paragraphs=doc.paragraphs
                positions=[]
                counter=""
                text=""
                number=0

                for paragraph in paragraphs:
                    text+=paragraph.text
                    positions.append({"start": len(counter), "end": len(text), "paragraph": number})
                    number+=1

                list_of_results.extend(appender(text, results, word, positions, model, False))

                    

        list_of_results.sort(key=lambda x: x["similarity"], reverse=True)

    db.close()
 
    return list_of_founds, list_of_results

