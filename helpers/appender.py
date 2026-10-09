from pathlib import Path
import re
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

def jaccard_similarity(a, b):
    a=set(a.split())
    b=set(b.split())

    return len(a&b)/len(a|b)

def appender(text, file, word, positions, model, go, in_need, limit):
    db=sqlite3.connect("zhorro.db")
    id=db.execute("SELECT id FROM files WHERE path=?", (str(file["path"]),)).fetchone()[0]
    suffix=Path(file["path"]).suffix
    results=[]
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

    if file["path"] in in_need:
        vectors=model.encode(chunks, batch_size=128)
        for i in range(length):
            cursor=db.execute("INSERT INTO chunks (file_id, text) VALUES (?,?)", (id, chunks[i]))
            chunk_id=cursor.lastrowid
            db.execute("INSERT INTO embeddings (chunk_id, embedding) VALUES (?,?)",(chunk_id, vectors[i].tobytes()))
        db.commit()

    else:
        rows=db.execute("SELECT embeddings.embedding FROM embeddings JOIN chunks ON chunks.id=embeddings.chunk_id WHERE chunks.file_id=?", (id,)).fetchall()
        vectors=[np.frombuffer(row[0], dtype=np.float32) for row in rows]

    query=model.encode(word)
    similarities = model.similarity(query, vectors)[0]
    remaining=text
    offset=0
            
    for i in range(length):
            
        leng=len(results)
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

        for j in range(leng):
            if jaccard_similarity(results[j]["chunk"], chunks[i])>=0.75:
                counter+=1
        if counter==0:
            if limit!=0:
                if len(results)<limit:
                    if suffix==".txt":
                        results.append({"chunk": chunks[i], "name": file["filename"], "start": start, "end": end, "similarity": round(similarities[i].item(), 3), "paragraph": None, "page": None, "suffix": suffix})

                    elif suffix==".docx":            
                        results.append({"chunk": chunks[i], "name": file["filename"], "start": start, "end": end, "similarity": round(similarities[i].item(), 3), "paragraph": position['paragraph']+1, "page": None, "suffix": suffix})

                    elif suffix==".pdf":
                        results.append({"chunk": chunks[i], "name": file["filename"], "start": start, "end": end, "similarity": round(similarities[i].item(), 3), "paragraph": None, "page": position['page']+1, "suffix": suffix})

            else:
                if suffix==".txt":
                    results.append({"chunk": chunks[i], "name": file["filename"], "start": start, "end": end, "similarity": round(similarities[i].item(), 3), "paragraph": None, "page": None, "suffix": suffix})

                elif suffix==".docx":            
                    results.append({"chunk": chunks[i], "name": file["filename"], "start": start, "end": end, "similarity": round(similarities[i].item(), 3), "paragraph": position['paragraph']+1, "page": None, "suffix": suffix})

                elif suffix==".pdf":
                    results.append({"chunk": chunks[i], "name": file["filename"], "start": start, "end": end, "similarity": round(similarities[i].item(), 3), "paragraph": None, "page": position['page']+1, "suffix": suffix})    

    return results