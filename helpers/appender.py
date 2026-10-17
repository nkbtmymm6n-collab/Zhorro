from pathlib import Path
import re
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

def jaccard_similarity(a, b):
    a=set(a.split())
    b=set(b.split())

    return len(a&b)/len(a|b)

def appender(text, file, word, positions, model, go, limit):
    db=sqlite3.connect("zhorro.db")
    id=db.execute("SELECT id FROM files WHERE path=?", (str(file["path"]),)).fetchone()[0]
    suffix=Path(file["path"]).suffix
    results=[]
    list_of_results=[]
    line_number=0

    if go:
        for position in positions:
            lines=text[position["start"]:position["end"]].splitlines()
            length=len(lines)
            previous=""
            for i in range(length):
                upcoming=""
                if i+1<length:
                    upcoming=lines[i+1]
                
                line_number+=1
                
                if i>0:
                    previous=lines[i-1]
                line=lines[i].lower()
                if word in line:
                    if limit!=0:
                        if len(file["contexts"])<limit:
                            counter=line.count(word)
                            new=word.upper()
                            if suffix==".txt":
                                file["contexts"].append({"line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming}) 

                            elif suffix==".docx":
                                file["contexts"].append({"paragraph": position["paragraph"]+1, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})

                            elif suffix==".pdf":
                                file["contexts"].append({"page": position["page"]+1, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})  
                    
                    else:
                        counter=line.count(word)
                        new=word.upper()
                        if suffix==".txt":
                            file["contexts"].append({"line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming}) 

                        elif suffix==".docx":
                            file["contexts"].append({"paragraph": position["paragraph"]+1, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})

                        elif suffix==".pdf":
                            file["contexts"].append({"page": position["page"]+1, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})  
                    
    query=model.encode(word)
    rows=db.execute("SELECT chunks.text, chunks.start_line, chunks.end_line, chunks.page, chunks.paragraph, embeddings.embedding FROM chunks JOIN embeddings ON chunks.id = embeddings.chunk_id WHERE chunks.file_id = ?", (id,)).fetchall()
    vectors=[np.frombuffer(row[5], dtype=np.float32) for row in rows]
    similarities=model.similarity(query, vectors)[0]
    indexes=np.argsort(similarities.numpy())[::-1]

    if limit!=0:
        indexes=indexes[:limit]

    for i in indexes:
        results.append({"path": file["path"], "chunk": rows[i][0], "start": rows[i][1], "end": rows[i][2], "page": rows[i][3], "paragraph": rows[i][4], "similarity": round(similarities[i].item(), 3)})

    list_of_results.append(results)
    db.close()
    return list_of_results