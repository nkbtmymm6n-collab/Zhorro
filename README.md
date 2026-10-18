# Zhorro

**Zhorro** is a local document search application that combines exact word search with semantic search.

It is designed to search through personal documents without uploading their contents to a cloud service.

Zhorro supports **TXT, DOCX and PDF** files and uses a local SQLite database to store indexed data and semantic embeddings.

---

## Features

- Exact word search
- Semantic search
- Support for TXT, DOCX and PDF files
- Local SQLite database
- GPU acceleration with CUDA when available
- CPU fallback when CUDA is unavailable
- Desktop graphical interface built with Qt Quick / QML
- Open source documents directly from search results
- Document contents are processed locally
- Modular Python + QML architecture

---

## How it works

Zhorro uses two complementary search methods.

### Exact search

When a query matches words stored in the index, Zhorro can find their occurrences in the selected documents and display their surrounding context.

For example:

```text
Previous line
CURRENT MATCH
Next line
```

For supported document formats, Zhorro can also provide additional information such as:

- line number
- paragraph number
- page number

### Semantic search

Zhorro converts text chunks into vector embeddings using a Sentence Transformer model.

The query is converted into an embedding and compared with stored document embeddings.

This allows Zhorro to find text that is **semantically related to the query**, even when the exact words are different.

---

## Supported file formats

| Format | Supported |
|--------|-----------|
| TXT    | Yes |
| DOCX   | Yes |
| PDF    | Yes |

---

## Architecture

```text
                         Zhorro
                            |
              +-------------+-------------+
              |                           |
           Frontend                    Backend
              |                           |
          Qt Quick / QML                Python
              |                           |
              |              +------------+------------+
              |              |            |            |
              |         Indexator       Finder      Database
              |              |            |            |
              |              +------------+------------+
              |                           |
              |                        SQLite
              |                           |
              |                       Embeddings
              |
              +--------------- QML / Python
```

---

## Project structure

```text
Zhorro/
|
├── main.py
├── main.qml
|
├── helpers/
│   ├── class_zhorro.py
│   ├── finder.py
│   ├── indexator.py
│   └── appender.py
|
├── interface/
│   ├── fonts/
│   ├── icons/
│   ├── designs/
│   └── pages/
|
├── zhorro.db
|
├── Zhorro_Architecture_EN.md
├── README.md
└── requirements.txt
```

---

## Backend

### Indexator

The indexator processes documents and stores their searchable data in SQLite.

The general indexing pipeline is:

```text
File
  |
Parse
  |
Extract text
  |
Extract words
  |
Create chunks
  |
Generate embeddings
  |
Store metadata
  |
SQLite database
```

The index contains:

- files
- words
- file-word relationships
- text chunks
- chunk metadata
- embeddings

### Finder

The finder handles search requests.

The general search pipeline is:

```text
Query
  |
Finder
  +-- Exact search
  |      |
  |   Contexts
  |
  +-- Semantic search
         |
      Embeddings
         |
      Similarity
         |
      Results
```

Exact search is useful when looking for a specific word.

Semantic search is useful when looking for a concept or meaning.

---

## Database

Zhorro uses SQLite.

The main tables are:

```text
files
words
word_files
chunks
embeddings
```

### `files`

Stores information about indexed documents.

```text
id
path
hash
```

### `words`

Stores unique indexed words.

```text
id
word
```

### `word_files`

Connects words with files.

```text
word_id
file_id
```

### `chunks`

Stores text chunks and their document positions.

```text
id
file_id
text
start_line
end_line
page
paragraph
```

### `embeddings`

Stores vector representations of chunks.

```text
id
chunk_id
embedding
```

---

## Technologies

Zhorro is built using:

- **Python** — backend
- **PySide6** — desktop application framework
- **Qt Quick / QML** — user interface
- **SQLite** — local database
- **Sentence Transformers** — semantic embeddings
- **PyMuPDF** — PDF processing
- **python-docx** — DOCX processing
- **NumPy** — numerical operations
- **PyTorch** — machine learning backend

---

## GPU acceleration

Zhorro can automatically select the available computing device.

The application checks whether CUDA is available:

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
```

If a compatible NVIDIA GPU is available, Zhorro uses CUDA.

Otherwise, it falls back to CPU.

---

## Running from source

### 1. Clone the repository

```bash
git clone <repository-url>
cd Zhorro
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run Zhorro

```powershell
python main.py
```

---

## Requirements

Zhorro requires Python and the dependencies listed in `requirements.txt`.

The main dependencies are:

```text
PySide6
sentence-transformers
torch
numpy
PyMuPDF
python-docx
```

The exact versions should be taken from `requirements.txt`.

---

## Indexing documents

To index documents:

1. Open Zhorro.
2. Select the documents you want to search.
3. Start indexing.
4. Zhorro processes the documents and stores the resulting data in SQLite.
5. The documents can then be searched.

Zhorro calculates a file hash to detect changes in previously indexed documents.

If a document has changed, its previous indexed data can be replaced with newly generated data.

---

## Search results

Search results can contain two types of matches.

### Exact matches

Exact matches show the location and surrounding context of the matching word.

```text
Previous text

CURRENT MATCH

Following text
```

### Semantic matches

Semantic matches display:

- the matching text chunk
- its position in the document
- similarity score

Example:

```text
Semantic matches

Similarity · 0.842

Relevant text from the document...
```

---

## Privacy

Zhorro is designed as a **local document search application**.

Document contents are processed locally by the application and stored in the local SQLite database.

No document upload service is required for the search functionality.

---

## Performance

Semantic indexing can be computationally expensive because embeddings have to be generated for document chunks.

For this reason, Zhorro supports GPU acceleration through CUDA when available.

Search and indexing operations are separated from the main Qt interface using worker threads so that long-running operations do not intentionally block the user interface.

---

## User interface

The interface is built with Qt Quick / QML.

The main UI components include:

- Greeting page
- Search page
- Indexing page
- Files page
- Result cards
- Sidebar
- Splash screen

The interface is separated from the Python backend.

Python handles:

- indexing
- searching
- database operations
- file management

QML handles:

- layout
- visual components
- animations
- user interaction
- displaying search results

---

## Building

Zhorro can be packaged into a standalone Windows application using **PyInstaller**.

A packaged version is intended to include the Python runtime and required Python dependencies so that Python does not need to be installed separately.

The QML interface, icons, fonts and other resources must also be included in the final build.

Build instructions will be documented once the packaging configuration is finalized.

---

## Project documentation

Additional technical documentation is available in:

```text
Zhorro_Architecture_EN.md
```

This document describes the internal architecture and data flow of the application in more detail.

---

## Development status

Zhorro is currently in active development.

The core functionality is implemented:

- document indexing
- SQLite storage
- exact search
- semantic search
- TXT/DOCX/PDF support
- QML interface
- asynchronous indexing
- asynchronous search
- GPU/CPU device selection

Future improvements may include:

- improved search performance
- UI optimization for very large result sets
- standalone application packaging
- installer
- additional document formats
- further search improvements

---

## License

This project is currently not licensed for redistribution.

A license will be added when the project is ready for public distribution.

---

## Author

**Zhorro**

A local document search project built with Python, PySide6, QML, SQLite and Sentence Transformers.
