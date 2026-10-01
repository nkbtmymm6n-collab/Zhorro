# Zhorro — Architecture Documentation

## Purpose

Zhorro is a local search engine for finding information in user documents.

Supported formats:
- TXT
- PDF
- DOCX

The main goal is to combine exact search with semantic search based on embeddings.

## Architecture

```text
User
 ↓
main()
 ↓
finder()
 ↓
┌────────────────┬──────────────────┐
│  Exact Search  │ Semantic Search  │
│     SQLite     │   Embeddings     │
└───────┬────────┴────────┬─────────┘
        ↓                  ↓
    Contexts          Ranked chunks
        └────────────┬─────┘
                     ↓
                 Results
```

For a single-word query, Zhorro uses hybrid search:
- exact search through SQLite;
- semantic search through embeddings.

For a phrase or question, Zhorro uses semantic search.

---

## Main Components

### `main()`

The entry point of the application.

Responsibilities:
1. Receive file paths from the user.
2. Create a `zhorro` object.
3. Scan and sort files.
4. Index new or changed files.
5. Run `finder()`.
6. Display direct and semantic results.

---

### `zhorro`

The class responsible for working with selected files.

#### `scan()`

Checks:
- whether the path exists;
- whether it is a file;
- whether its extension is supported.

The resulting files are stored in `self.files`.

#### `sort()`

Classifies files into:
- `self.txt`
- `self.docx`
- `self.pdf`

#### `index()`

Uses SHA-256 hashes to determine:
- new files;
- modified files.

New or modified files are stored or updated in SQLite.

---

## SQLite Database

### `files`

Stores file information:

```text
id
path
hash
```

`id` is an autoincrementing primary key.

`hash` contains the SHA-256 hash of the file contents.

The hash is used to detect whether a file has changed since the last indexing operation.

---

### `words`

Stores unique words:

```text
id
word
```

The `word` column is unique.

---

### `word_files`

Connects words and files:

```text
word_id
file_id
```

The pair `(word_id, file_id)` is unique.

This prevents duplicate word-file relationships.

---

## `indexator()`

`indexator()` extracts text from new or modified files and creates the word-to-file index.

### TXT

Text is read directly using UTF-8.

### PDF

Text is extracted using PyMuPDF.

### DOCX

Text is extracted using `python-docx`.

Words are converted to lowercase and stored in the `words` table.

Relationships between words and files are stored in `word_files`.

`INSERT OR IGNORE` is used to avoid duplicate entries.

---

# `finder()`

`finder()` determines which search mode to use.

## Single-word query

Example:

```text
python
```

The search is hybrid:

```text
SQLite exact search
        +
semantic search
```

SQLite first identifies files that contain the requested word.

Then `appender()`:
- finds exact occurrences;
- creates contexts;
- performs semantic search over the file content.

---

## Phrase or question

Example:

```text
how does file handling work in Python
```

Semantic search is performed across all indexed files.

---

# `appender()`

`appender()` processes the text of a specific file, PDF page, or DOCX paragraph.

Signature:

```python
appender(text, file, word, number, model, go)
```

### `go`

Controls whether exact search is additionally performed.

```text
go=True
    ↓
exact + semantic

go=False
    ↓
semantic only
```

---

## Exact Search

The text is split into lines:

```python
lines = text.splitlines()
```

Each line is checked for the requested word.

For every match, Zhorro stores:

```python
{
    "line_number": ...,
    "amount": ...,
    "previous": ...,
    "current": ...,
    "upcoming": ...
}
```

DOCX results additionally contain the paragraph number.

PDF results additionally contain the page number.

---

# Semantic Search

The text is divided into chunks of approximately 50 words.

The current implementation uses punctuation as chunk boundaries:

```text
. ! ? , ; : —
```

Each chunk is converted into an embedding using:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

The user's query is also converted into an embedding.

Similarity between the query and each chunk is then calculated.

Results are sorted by similarity in `finder()`:

```python
list_of_results.sort(
    key=lambda x: x["similarity"],
    reverse=True
)
```

The most semantically similar chunks therefore appear first.

---

# Mapping Chunks Back to the Source Document

An important part of Zhorro is determining where a semantic chunk came from in the original document.

The chunk is searched for in the original text using `re.search()`.

The start and end line numbers are calculated from the character positions:

```python
start = text[:starting].count("\n") + 1
end = text[:ending].count("\n") + 1
```

Semantic results contain:

```python
{
    "chunk": ...,
    "start": ...,
    "end": ...,
    "similarity": ...,
    "paragraph": ...,
    "page": ...,
    "suffix": ...
}
```

The search position is advanced through the remaining text so repeated identical chunks can still be mapped to different locations.

---

# Search Flow

## Exact Search

```text
Query
 ↓
SQLite
 ↓
Files containing the word
 ↓
appender()
 ↓
Contexts
 ↓
main()
 ↓
Display
```

## Semantic Search

```text
Query
 ↓
Query embedding
 ↓
Document chunks
 ↓
Chunk embeddings
 ↓
Similarity
 ↓
Sorting
 ↓
Results
```

---

# Current Development Areas

Planned improvements include:

- better natural-language query understanding;
- query rewriting / query expansion;
- improved result ranking;
- filtering low-similarity results;
- storing embeddings during indexing;
- improved chunking;
- chunk overlap;
- better preservation of PDF/DOCX structure;
- GUI;
- search-quality testing.

---

# Planned Architecture

```text
User Query
    ↓
Query Understanding
    ↓
Hybrid / Semantic Retrieval
    ↓
Ranking
    ↓
Top Results
    ↓
GUI
```

The long-term goal is to keep Zhorro as a local search system for user files while gradually adding more intelligent query understanding and retrieval.
