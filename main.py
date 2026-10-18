import sys
import os
import torch
import sqlite3
from pathlib import Path
from helpers.class_zhorro import zhorro
from helpers.finder import finder
from helpers.indexator import indexator
from PySide6.QtGui import QPixmap
from sentence_transformers import SentenceTransformer
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, Property, QThread
from PySide6.QtWidgets import QApplication, QFileDialog, QSplashScreen


app=QApplication(sys.argv)
splash_engine=QQmlApplicationEngine()
splash_engine.load("interface/designs/Splash.qml")

if not splash_engine.rootObjects():
    sys.exit(-1)

splash=splash_engine.rootObjects()[0]
app.processEvents()
device = "cuda" if torch.cuda.is_available() else "cpu"
model=SentenceTransformer("all-MiniLM-L6-v2", device=device)
splash.close()

class IndexWorker(QObject):
    searchFinished=Signal(list, list)
    finished=Signal(bool)

    def __init__(self, files):
        super().__init__()
        self.files=files

    @Slot()
    def run(self):
        try:

            zhorros=zhorro(self.files)
            zhorros.scan()

            new=zhorros.checker()

            indexator(new, model)
            self.finished.emit(True)

        except Exception as e:
            print("INDEX ERROR:", repr(e))
            self.finished.emit(False)

    @Slot(str, int, list)
    def search(self, query, limit, selected):
        try:
            exact, semantic=finder(query, model, limit, selected)
            self.searchFinished.emit(exact, semantic)
        except Exception as e:
            print("SEARCH ERROR:", repr(e))

class Backend(QObject):

    filesChanged=Signal(list)
    need2Show=Signal(list)
    filesSelected=Signal(list)
    counterChanged=Signal(int)
    exactResultsChanged=Signal(list)
    semanticResultsChanged=Signal(list)
    selectionChanged=Signal()
    filesCounterChanged=Signal(int)
    resultsCounterChanged=Signal(int)
    resultsChanged=Signal(list)
    indexFinished=Signal(bool)
    searchFinished=Signal(list, list)

    def __init__(self):
        super().__init__()
        self.files=[]
        self.shows=[]
        self._selected=[]
        self._counter=0
        self._filesCounter=0
        self._resultsCounter=0
        self._exactResults=[]
        self._semanticResults=[]
        self._results=[]
        self.counterChanged.emit(self._counter)

    @Slot(bool)
    def indexFinishedSlot(self, success):
        self.indexFinished.emit(success)

    @Property(list, notify=exactResultsChanged)
    def exactResults(self):
        return self._exactResults

    @Property(list, notify=resultsChanged)
    def results(self):
        return self._results

    @Property(list, notify=selectionChanged)
    def selected(self):
        return self._selected

    @Property(list, notify=semanticResultsChanged)
    def semanticResults(self):
        return self._semanticResults

    @Property(int, notify=filesCounterChanged)
    def fileCounter(self):
        return self._filesCounter

    @Property(int, notify=resultsCounterChanged)
    def resultsCounter(self):
        return self._resultsCounter

    @Slot()
    def reset(self):
        self._exactResults=[]
        self._semanticResults=[]
        self._results=[]
        self.exactResultsChanged.emit(self._exactResults)
        self.semanticResultsChanged.emit(self._semanticResults)
        self.resultsChanged.emit(self._results)

    @Property(int, notify=counterChanged)
    def counter(self):
        return self._counter

    @Slot(str, result=bool)
    def isSelected(self, path):
        return path in self._selected
        
    @Slot(int)
    def count(self, inp):
        if inp==1:
            self._counter+=1
        else:
            if self._counter!=0:
                self._counter-=1
        self.counterChanged.emit(self._counter)

    @Slot(str)
    def search(self, query):

        self.thread=QThread()
        self.worker=IndexWorker([])

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(lambda: self.worker.search(query, self._counter, self._selected.copy()))

        self.worker.searchFinished.connect(self.searchFinishedSlot)

        self.worker.searchFinished.connect(self.thread.quit)
        self.worker.searchFinished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    @Slot(list, list)
    def searchFinishedSlot(self, exact, semantic):

        self._exactResults=exact
        self._semanticResults=semantic

        self._results=[]

        for exact_file in self._exactResults:

            self._results.append({"path": exact_file["path"], "filename": exact_file["filename"],"exact": exact_file["contexts"], "semantic": []})
                

        for semantic_group in self._semanticResults:

            if not semantic_group:
                continue

            path=semantic_group[0]["path"]

            found=False

            for result in self._results:

                if result["path"]==path:

                    result["semantic"]=semantic_group
                    found=True
                    break

            if not found:

                self._results.append({"path": path, "filename": semantic_group[0]["filename"], "exact": [], "semantic": semantic_group})

        self._filesCounter=len(self._results)

        self._resultsCounter=0

        for file in self._results:
            self._resultsCounter+=len(file["exact"])
            self._resultsCounter+=len(file["semantic"])

        self.exactResultsChanged.emit(self._exactResults)
        self.semanticResultsChanged.emit(self._semanticResults)
        self.filesCounterChanged.emit(self._filesCounter)
        self.resultsCounterChanged.emit(self._resultsCounter)
        self.resultsChanged.emit(self._results)
            
            

    @Slot(str, result=bool)
    def manager(self, path):
        if path in self._selected:
            self._selected.remove(path)
            db.execute("DELETE FROM embeddings WHERE chunk_id IN (SELECT id FROM chunks WHERE file_id = (SELECT id FROM files WHERE path = ?))", (path,))
            db.execute("DELETE FROM chunks WHERE file_id = (SELECT id FROM files WHERE path = ?)", (path,))
            db.execute("DELETE FROM word_files WHERE file_id = (SELECT id FROM files WHERE path = ?)", (path,))
            db.execute("DELETE FROM files WHERE path = ?", (path,))
            self.selectionChanged.emit()
            return False
        
        else:
            self._selected.append(path)
            self.selectionChanged.emit()
            return True
    
    @Slot()
    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(None, "Select files", "", "Documents (*.txt *.docx *.pdf)")

        self.files.extend(files)

        self.filesChanged.emit(self.files)

    @Slot()
    def index(self):

        self.thread = QThread()
        self.worker = IndexWorker(self.files.copy())

        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.indexFinishedSlot)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

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
        self.shows.remove(path)
        if path in self._selected:
            self._selected.remove(path)
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
        os.startfile(str(path))



db=sqlite3.connect("zhorro.db")


db.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT NOT NULL, hash TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS word_files (word_id INTEGER, file_id INTEGER, UNIQUE(word_id, file_id))")
db.execute("CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER NOT NULL, text TEXT NOT NULL, start_line INTEGER, end_line INTEGER, page INTEGER, paragraph INTEGER, FOREIGN KEY (file_id) REFERENCES files(id))")
db.execute("CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY AUTOINCREMENT, chunk_id INTEGER NOT NULL UNIQUE, embedding BLOB NOT NULL, FOREIGN KEY (chunk_id) REFERENCES chunks(id))")
paths=[]

engine = QQmlApplicationEngine()
backend = Backend()
engine.rootContext().setContextProperty("backend", backend)
engine.load("main.qml")

if not engine.rootObjects():
    sys.exit(-1)

splash.close()
splash_engine=None

sys.exit(app.exec())