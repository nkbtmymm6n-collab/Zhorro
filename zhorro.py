import sqlite3
from pathlib import Path
from helpers.class_zhorro import zhorro
from helpers.finder import finder
from helpers.indexator import indexator

def main():
    db=sqlite3.connect("zhorro.db")
    db.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT NOT NULL, hash TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS word_files (word_id INTEGER, file_id INTEGER, UNIQUE(word_id, file_id))")
    paths=[]
    path=input("Input path: ")

    while path!="":
        paths.append(path)
        path=input("Input path: ")

    paths=zhorro(paths)
    paths.scan()
    print("FILES:", paths.files)
    paths.sort()
    paths.index()
    print("NEW:", paths.new)
    indexator(paths.new)

    files, results=finder(input("Input what you wanna find (it could be a single word, a phrase or an explanation of what's being sought): ").lower())
    if len(files)>0:

        print("Direct Search:")
        for file in files:
            suffix=Path(file["path"]).suffix
            print(f"Your word is in {file['filename']}")
            print("")
            print(f"It's location is {file['path']}")
            print("")
            print("")
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
                print(f"Paragraph {result['paragraph']}")


            elif result["suffix"]==".pdf":
                print(f"Page {result['page']}")

            print(f"From line {result['start']} to line {result['end']}")
            print("")
            print(result['chunk'])



if __name__=="__main__":
    main()
