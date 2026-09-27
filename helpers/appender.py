from pathlib import Path

def appender(text, file, word, number):
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
