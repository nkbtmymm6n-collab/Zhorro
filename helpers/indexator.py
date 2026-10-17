import sqlite3
import re
import numpy as np
import pymupdf
from pathlib import Path
from docx import Document

def indexator(paths, model):

    db=sqlite3.connect("zhorro.db")

    for path in paths:
        path=Path(path)
        words=[]
        positions=[]
        text=""
        suffix=path.suffix.lower()
        file_id=db.execute("SELECT id FROM files WHERE path=?",(str(path),)).fetchone()[0]
        

        if suffix==".txt":
        
            with open(path, "r", encoding="utf-8") as file:
                text=file.read()
                words.extend(text.split())
                length=len(words)
                for i in range(length):
                    words[i]=words[i].strip(".,!?;:()[]{}\"'«»—-")

        elif suffix==".pdf":

            doc = pymupdf.open(path)
            
            positions=[]
            number=0
            counter=""
            text=""
            for page in doc:
                text1=page.get_text()
                words.extend(text1.split())
                text+=page.get_text()
                positions.append({"start": len(counter), "end": len(text), "page": number})
                counter=text
                number+=1

            length=len(words)
            for i in range(length):
                words[i]=words[i].strip(".,!?;:()[]{}\"'«»—-")

            doc.close()

        elif suffix==".docx":

            doc=Document(path)
            positions=[]
            number=0
            counter=""
            text=""
            for paragraph in doc.paragraphs:
                text1=paragraph.text
                words.extend(text1.split())
                text+=paragraph.text + "\n"
                positions.append({"start": len(counter), "end": len(text), "paragraph": number})
                counter=text
                number+=1

            length=len(words)

            for i in range(length):
                words[i]=words[i].strip(".,!?;:()[]{}\"'«»—-")
        for word in words:
            word=word.lower()
            db.execute(
                "INSERT OR IGNORE INTO words (word) VALUES (?)",
                (word,)
            )

            word_id = db.execute(
                "SELECT id FROM words WHERE word = ?",
                (word,)
            ).fetchone()[0]

            cursor = db.execute(
                "INSERT OR IGNORE INTO word_files (word_id, file_id) VALUES (?, ?)",
                (word_id, file_id)
            )

        db.commit()

        sentences=re.split(r'(?<=[.!?,;:—])', text)
        amount=len(sentences)
        chunks=[]
        j=0
        subchunk=""
        length=0

        for i in range(amount):
                length+=len(sentences[i].split())

        while True:
                    
                while j<amount and len(subchunk.split())<50:
                    subchunk+=sentences[j]
                    j+=1 
                    if len(subchunk.split())>=50:
                        break
                            
                chunks.append(subchunk)
                subchunk=""
                if j==amount:
                    break

        length=len(chunks)
        row=db.execute("SELECT 1 FROM embeddings JOIN chunks ON chunks.id = embeddings.chunk_id JOIN files ON files.id = chunks.file_id WHERE files.path = ? LIMIT 1", (str(path),)).fetchone()
        chunk_ids=[]
        if row is None:
            vectors=model.encode(chunks, batch_size=128)
            for i in range(length):
                cursor=db.execute("INSERT INTO chunks (file_id, text) VALUES (?,?)", (file_id, chunks[i]))
                chunk_id=cursor.lastrowid
                chunk_ids.append(chunk_id)
                db.execute("INSERT INTO embeddings (chunk_id, embedding) VALUES (?,?)",(chunk_id, vectors[i].tobytes()))
            db.commit()

        else:
            rows = db.execute("SELECT chunks.id, embeddings.embedding FROM embeddings JOIN chunks ON chunks.id = embeddings.chunk_id WHERE chunks.file_id = ?", (file_id,)).fetchall()

            chunk_ids=[row[0] for row in rows]

            vectors=[np.frombuffer(row[1], dtype=np.float32) for row in rows]

        remaining=text
        offset=0
                
        for i in range(length):
            counter=0
            match=re.search(re.escape(chunks[i]), remaining)
            start=None
            end=None
            position=None
            if match:
                    
                starting=offset+match.start()
                ending=offset+match.end()

                before=text[:starting]
                after=text[:ending]

                start=before.count("\n")+1
                end=after.count("\n")+1

                remaining=remaining[match.end():]

                offset+=match.end()
                position = None

                for pos in positions:

                    if pos["start"] <= starting < pos["end"]:
                        position=pos
                        break
                
                if path.suffix==".pdf":
                    db.execute("UPDATE chunks SET start_line = ?, end_line = ?, page = ?, paragraph = ? WHERE id = ?", (start, end, position["page"], None, chunk_ids[i]))

                elif path.suffix==".docx":
                    db.execute("UPDATE chunks SET start_line = ?, end_line = ?, page = ?, paragraph = ? WHERE id = ?", (start, end, None, position["paragraph"], chunk_ids[i]))

                else:
                    db.execute("UPDATE chunks SET start_line = ?, end_line = ?, page = ?, paragraph = ? WHERE id = ?", (start, end, None, None, chunk_ids[i]))
        
    db.commit()
    db.close()
            
        
