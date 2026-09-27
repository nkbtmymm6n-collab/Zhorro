import sqlite3
from pathlib import Path
from helpers.class_zhorro import zhorro
from helpers.finder import finder
from helpers.indexator import indexator

def main():
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
    files=finder(input("Input the word that you need to find: ").lower())

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

    db=sqlite3.connect("zhorro.db")
    db.execute("DELETE FROM word_files")
    db.execute("DELETE FROM words")
    db.execute("DELETE FROM files")
    db.commit()
    db.close()


if __name__=="__main__":
    main()
