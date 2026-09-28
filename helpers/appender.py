import sqlite3
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer

def appender(text, file, word, number, model):
    db=sqlite3.connect("zhorro.db")
    lines=text.splitlines()
    length=len(lines)
    previous=""
    suffix=Path(file["path"]).suffix
    for i in range(length):
        upcoming=""
        if i+1<length:
            upcoming=lines[i+1]
    
        line_number=i+1
    
        if i>0:
            previous=lines[i-1]
        line=lines[i].lower()
        if word in line:
            counter=line.count(word)
            new=word.upper()
            if suffix==".txt":
                file["contexts"].append({"line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming}) 

            elif suffix==".docx":
                file["contexts"].append({"paragraph": number, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})

            elif suffix==".pdf":
                 file["contexts"].append({"page": number, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})  

    sentences=re.split(r'[.!?,;:—]+', text)
    amount=len(sentences)
    chunks=[]
    j=0
    subchunk=""
    results=[]
    length=0

    for i in range(amount):
        length+=len(sentences[i].split())

    while True:
        
        while j<amount and len(subchunk.split())<50 and len(subchunk.split())<=length:
            subchunk+=sentences[j]
            j+=1 
            if len(subchunk.split())>=50:
                break
                
        chunks.append(subchunk)
        subchunk=""
        if j==amount:
            break

    vectors=model.encode(chunks)
    query=model.encode(word)
    similarities = model.similarity(query, vectors)
    length=len(chunks)
    for i in range(length):
        if suffix==".txt":
            results.append({"chunk": chunks[i], "start": start, "end": end, "similarity": similarities[i], "paragraph": None, "page": None})

        elif suffix==".docx":            
             results.append({"chunk": chunks[i], "start": start, "end": end, "similarity": similarities[i], "paragraph": number, "page": None})

        elif suffix==".pdf":
             results.append({"chunk": chunks[i], "start": start, "end": end, "similarity": similarities[i], "paragraph": None, "page": number})