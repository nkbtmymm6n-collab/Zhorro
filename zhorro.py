import sqlite3
from pathlib import Path
from helpers.class_zhorro import zhorro
from helpers.finder import finder
from helpers.indexator import indexator
from sentence_transformers import SentenceTransformer

def main():
    model=SentenceTransformer("all-MiniLM-L6-v2")
    db=sqlite3.connect("zhorro.db")
    db.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT NOT NULL, hash TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS word_files (word_id INTEGER, file_id INTEGER, UNIQUE(word_id, file_id))")
    db.execute("CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER NOT NULL, text TEXT NOT NULL, FOREIGN KEY (file_id) REFERENCES files(id))")
    db.execute("CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY AUTOINCREMENT, chunk_id INTEGER NOT NULL UNIQUE, embedding BLOB NOT NULL, FOREIGN KEY (chunk_id) REFERENCES chunks(id))")
    paths=[]
    path=input("Input path: ")

    while path!="":
        paths.append(path)
        path=input("Input path: ")

    paths=zhorro(paths)
    paths.scan()
    paths.sort()
    paths.index()
    indexator(paths.new)

    while True:
        validator=input("Do you wanna know the contexts? [y/n]:")
        if validator!="y" and validator!="n":
            print("Please input either y or n.")
        else:
            break

    while True:
        try:
            limit=int(input("How many results per file do you want me to show? (0 = all): "))
            if limit<0:
                 print("Input a non-negative integer.")
            else:
                break
        except ValueError:
            print ("Input a non-negative integer.")
        
    
    files, results=finder(input("Input what you wanna find (it could be a single word, a phrase or an explanation of what's being sought): ").lower(), model, paths.new, limit)

    if len(files)>0:

        print("Direct Search:")
        for file in files:
            suffix=Path(file["path"]).suffix
            print(f"Your word is in {file['filename']}")
            print("")
            print(f"It's location is {file['path']}")
            print("")
            print("")

            if validator=="y":

                print("Contexts:")

                for context in file["contexts"]:
                    if suffix==".docx":
                        print(f"Paragraph {context['paragraph']}, {context['amount']} times")
                    elif suffix==".pdf":
                        print(f"Page {context['page']}")
                    if suffix==".pdf" or suffix==".txt":
                        print(f"Line {context['line_number']}, {context['amount']} times")
                    print(context["previous"])
                    print(context["current"])
                    print(context["upcoming"])
                    print("")
                    print("")

    if len(results)>0:
        
        print("Semantic Search:")
        for result in results:
            if result["suffix"]==".docx":
                print(f"{result['name']}, paragraph {result['paragraph']}")


            elif result["suffix"]==".pdf":
                print(f"{result['name']}, page {result['page']}")
            
            print(f"Similarity: {result['similarity']}")
            print("")

            if validator=="y":
        
                print(result['chunk'])
                print("")

    if len(results)==0 and len(files)==0:
        print("Unfortunately, Zhorro couldn't find any match in these files. ")



if __name__=="__main__":
    main()
