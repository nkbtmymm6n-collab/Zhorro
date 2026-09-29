import sqlite3
import hashlib
from docx import Document
from pathlib import Path

class zhorro:

    def __init__(self, paths):
        self.paths = paths 
        self.files = []
        self.txt = []
        self.docx = []
        self.pdf = []
        self.new=[]

    def scan(self):

        final=[]

        for path in self.paths:
            path=Path(path)

            if not path.exists():
                print(f"Skipping {path} as it does not exist.\n")
            
            elif not path.is_file():
                print(f"Skipping {path} as it is not a file.\n")

            elif path.suffix.lower() not in [".txt", ".docx", ".pdf"]:
                print(f"Skipping {path} as it is not a supported file type.\n")

            else:
                final.append(path)

        self.files = final
        return self.files

    def sort(self):

        for path in self.files:

            if path.suffix.lower() == ".txt":
                self.txt.append(path)

            elif path.suffix.lower() == ".docx":
                self.docx.append(path)

            elif path.suffix.lower() == ".pdf":
                self.pdf.append(path)
        
        return self.txt, self.docx, self.pdf

    def index(self):
        self.new=[]
        db = sqlite3.connect("zhorro.db")
        for file in self.files:
            h = hashlib.sha256()
            

            with open (file, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
                file_hash=h.hexdigest()

            row=db.execute("SELECT id, hash FROM files WHERE path=?",(str(file),)).fetchone()

            if row is None:
                db.execute("INSERT INTO files (path, hash) VALUES (?, ?)", (str(file), file_hash))
                self.new.append(file)
            

            elif row[1]!=file_hash:
                db.execute("DELETE FROM word_files  WHERE file_id=?", (row[0],))             
                db.execute("UPDATE files SET hash=? WHERE path=?", (file_hash, str(file)))
                self.new.append(file)
        
        db.commit()
        db.close()
        return self.new