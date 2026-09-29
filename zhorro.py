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
    print("FILES:", paths.files)
    paths.sort()
    paths.index()
    print("NEW:", paths.new)
    indexator(paths.new)

    files, results=finder(input("Input the word that you need to find: ").lower())

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

    print("Semnatic Search:")
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
