import sys
import os
import sqlite3
from pathlib import Path
from helpers.class_zhorro import zhorro
from helpers.finder import finder
from helpers.indexator import indexator
from sentence_transformers import SentenceTransformer
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication, QFileDialog


app=QApplication(sys.argv)
model=SentenceTransformer("all-MiniLM-L6-v2")

class Backend(QObject):

    filesChanged=Signal(list)
    need2Show=Signal(list)

    def __init__(self):
        super().__init__()
        self.files=[]
        self.shows=[]
        self.selected=[]

    @Slot(str)
    def search(self, query):
        ...
    
    @Slot()
    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(None, "Select files", "", "Documents (*.txt *.docx *.pdf)")

        self.files.extend(files)
        self.filesChanged.emit(self.files)

    @Slot(result=bool)
    def index(self):
        try:
            zhorros=zhorro(self.files)
            zhorros.scan()
            new=zhorros.checker()
            indexator(new)
            return True
        except Exception as e:
            print(e)
            return False

    @Slot(str)
    def delete(self, name):
            if name in self.files: 
                self.files.remove(name)
                self.filesChanged.emit(self.files)

    @Slot()
    def clearFiles(self):
        self.files.clear()
        self.filesChanged.emit(self.files)  

    @Slot(str)
    def erase(self, path):
        db.execute("DELETE FROM embeddings WHERE chunk_id IN (SELECT id FROM chunks WHERE file_id = (SELECT id FROM files WHERE path = ?))", (path,))
        db.execute("DELETE FROM chunks WHERE file_id = (SELECT id FROM files WHERE path = ?)", (path,))
        db.execute("DELETE FROM word_files WHERE file_id = (SELECT id FROM files WHERE path = ?)", (path,))
        db.execute("DELETE FROM files WHERE path = ?", (path,))
        db.commit()

    @Slot()
    def show(self):
        
        db=sqlite3.connect("zhorro.db")
        files=db.execute("SELECT path FROM files").fetchall()
        files=[file[0] for file in files]
        self.shows=files
        self.need2Show.emit(self.shows)

    @Slot(str)
    def open(self, path):
        os.startfile(path)



db=sqlite3.connect("zhorro.db")
db.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT NOT NULL, hash TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS word_files (word_id INTEGER, file_id INTEGER, UNIQUE(word_id, file_id))")
db.execute("CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER NOT NULL, text TEXT NOT NULL, FOREIGN KEY (file_id) REFERENCES files(id))")
db.execute("CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY AUTOINCREMENT, chunk_id INTEGER NOT NULL UNIQUE, embedding BLOB NOT NULL, FOREIGN KEY (chunk_id) REFERENCES chunks(id))")
paths=[]

engine = QQmlApplicationEngine()
backend = Backend()
engine.rootContext().setContextProperty("backend", backend)
engine.load("main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())