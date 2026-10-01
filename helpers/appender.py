from pathlib import Path
import re
from sentence_transformers import SentenceTransformer

def jaccard_similarity(a, b):
    a=set(a.split())
    b=set(b.split())

    return len(a&b)/len(a|b)

def appender(text, file, word, positions, model, go):
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
                    counter=line.count(word)
                    new=word.upper()
                    if suffix==".txt":
                        file["contexts"].append({"line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming}) 

                    elif suffix==".docx":
                        file["contexts"].append({"paragraph": position["paragraph"]+1, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})

                    elif suffix==".pdf":
                        file["contexts"].append({"page": position["page"]+1, "line_number": line_number, "amount": counter, "previous": previous, "current": lines[i].lower().replace(word, new), "upcoming": upcoming})  


    sentences=re.split(r'[.!?,;:—]+', text)
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

    vectors=model.encode(chunks)
    query=model.encode(word)
    similarities = model.similarity(query, vectors)[0]
    length=len(chunks)
    remaining=text
    offset=0
            
    for i in range(length):
        if len(results)>10:
            return results
        leng=len(results)
        counter=0
        match=re.search(re.escape(chunks[i]), remaining)
        start=None
        end=None
        if match:
                
            starting=offset+match.start()
            ending=offset+match.end()

            before=text[:starting]
            after=text[:ending]

            start=before.count("\n")+1
            end=after.count("\n")+1

            remaining=remaining[match.end():]

            offset+=match.end()

        for j in range(leng):
            if jaccard_similarity(results[j]["chunk"], chunks[i])>=0.75:
                counter+=1
        if counter==0:
            
            if suffix==".txt":
                results.append({"chunk": chunks[i], "start": start, "end": end, "similarity": similarities[i], "paragraph": None, "page": None, "suffix": suffix})

            elif suffix==".docx":            
                results.append({"chunk": chunks[i], "start": start, "end": end, "similarity": similarities[i], "paragraph": position['paragraph']+1, "page": None, "suffix": suffix})

            elif suffix==".pdf":
                results.append({"chunk": chunks[i], "start": start, "end": end, "similarity": similarities[i], "paragraph": None, "page": position['page']+1, "suffix": suffix})
                    
    return results