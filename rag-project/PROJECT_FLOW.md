# RAG Chat — Project Documentation

## What is RAG?

RAG stands for **Retrieval-Augmented Generation**. Instead of asking an LLM to answer from its training data alone, RAG first **retrieves relevant pieces of your document** and feeds them as context to the LLM. This means the model answers based on *your* document, not general knowledge.

---

## Project Structure

```
rag-project/
├── app.py              # Flask web server — handles HTTP routes
├── rag.py              # Core RAG logic — indexing, embedding, retrieval
├── templates/
│   └── index.html      # Frontend UI (chat interface)
├── uploads/            # Uploaded documents are saved here
├── .env                # API keys (GROQ_API_KEY)
└── requirements.txt    # Python dependencies
```

---

## Tech Stack

| Layer       | Tool / Library                        | Purpose                              |
|-------------|---------------------------------------|--------------------------------------|
| Web Server  | Flask                                 | Serves UI, handles upload & chat API |
| Embeddings  | `sentence-transformers` (MiniLM-L6)   | Converts text chunks into vectors    |
| Vector Store| FAISS (faiss-cpu)                     | Stores & searches vectors            |
| LLM         | Groq API (`llama-3.3-70b-versatile`)  | Generates answers from context       |
| PDF Parsing | pypdf                                 | Extracts text from PDF files         |
| Frontend    | Vanilla HTML/CSS/JS                   | Chat UI in the browser               |

---

## Full Project Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        UPLOAD FLOW                              │
│                                                                 │
│  User selects PDF/TXT                                           │
│         │                                                       │
│         ▼                                                       │
│  POST /upload  ──►  app.py saves file to /uploads/             │
│         │                                                       │
│         ▼                                                       │
│  rag.build_index(file_path)                                     │
│         │                                                       │
│         ├──► load_documents()                                   │
│         │       ├── PDF? → pypdf extracts text page by page     │
│         │       └── TXT? → reads raw text                       │
│         │       └── Splits full text into 500-char chunks       │
│         │                                                       │
│         ├──► embedder.encode(chunks)                            │
│         │       └── MiniLM-L6-v2 converts each chunk           │
│         │           into a 384-dim float vector                 │
│         │                                                       │
│         └──► faiss.IndexFlatL2.add(embeddings)                  │
│                 └── All vectors stored in FAISS index           │
│                     (in-memory, ready for search)               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         CHAT FLOW                               │
│                                                                 │
│  User types a question and hits Send                            │
│         │                                                       │
│         ▼                                                       │
│  POST /chat  ──►  app.py receives { "query": "..." }           │
│         │                                                       │
│         ▼                                                       │
│  rag.retrieve(query, top_k=3)                                   │
│         │                                                       │
│         ├──► embedder.encode([query])                           │
│         │       └── Query converted to a 384-dim vector        │
│         │                                                       │
│         ├──► faiss_index.search(query_vec, k=3)                 │
│         │       └── Finds 3 nearest chunk vectors               │
│         │           using L2 (Euclidean) distance               │
│         │                                                       │
│         └──► Returns top 3 matching text chunks                 │
│                                                                 │
│         ▼                                                       │
│  app.py builds prompt:                                          │
│         ├── System message: "Answer using only this context:"   │
│         │       + [chunk1] + [chunk2] + [chunk3]                │
│         └── User message: original query                        │
│                                                                 │
│         ▼                                                       │
│  Groq API call → llama-3.3-70b-versatile                        │
│         └── LLM reads context + question → generates answer    │
│                                                                 │
│         ▼                                                       │
│  JSON response { "answer": "..." } sent back to browser        │
│         │                                                       │
│         ▼                                                       │
│  UI renders answer in chat bubble                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Explanation

### 1. Document Upload & Chunking (`rag.py → load_documents`)

When a file is uploaded, the text is extracted and split into **500-character chunks**. Chunking is necessary because:
- Embedding models have input size limits
- Smaller chunks = more precise retrieval
- You only send *relevant* pieces to the LLM, not the whole document

```
"The quick brown fox jumps over the lazy dog. It was a sunny day..."
        ↓ split every 500 chars
["The quick brown fox jumps...", "It was a sunny day...", ...]
```

---

### 2. Embedding (`rag.py → build_index`)

Each chunk is passed through **`all-MiniLM-L6-v2`**, a lightweight sentence transformer model. It converts text into a **384-dimensional vector** — a list of numbers that captures the *semantic meaning* of the text.

```
"What is the refund policy?" → [0.12, -0.45, 0.88, ... ] (384 numbers)
```

Similar meaning = vectors that are close together in space.

---

### 3. FAISS Vector Index (`rag.py → build_index`)

All chunk vectors are stored in a **FAISS `IndexFlatL2`** index. FAISS is a high-performance library by Meta for similarity search. `IndexFlatL2` uses **Euclidean (L2) distance** — the closer two vectors, the more semantically similar the text.

---

### 4. Query Retrieval (`rag.py → retrieve`)

When the user asks a question:
1. The query is embedded into a vector using the same MiniLM model
2. FAISS searches the index for the **3 nearest vectors** (top_k=3)
3. The corresponding text chunks are returned

This ensures only the most relevant parts of the document are used — not the entire file.

---

### 5. LLM Answer Generation (`app.py → /chat`)

The retrieved chunks are joined and injected into the **system prompt**:

```
System: You are a helpful assistant. Answer using only the provided context.

Context:
[chunk 1 text]
[chunk 2 text]
[chunk 3 text]

User: What is the refund policy?
```

This is sent to **Groq's `llama-3.3-70b-versatile`** model. The LLM reads the context and generates a grounded answer. If the answer isn't in the context, it says so.

---

### 6. Frontend (`templates/index.html`)

The UI is a single-page chat interface that:
- Uploads files via `POST /upload` using `FormData`
- Sends queries via `POST /chat` with JSON
- Displays messages as styled chat bubbles with a typing indicator while waiting

---

## Data Flow Summary

```
PDF/TXT File
    │
    ▼
Text Extraction (pypdf / open())
    │
    ▼
Chunking (500 chars each)
    │
    ▼
Embedding (MiniLM-L6-v2) → 384-dim vectors
    │
    ▼
FAISS Index (stored in memory)
    │
    │◄─── User Query → Embedded → Nearest 3 chunks retrieved
    │
    ▼
Groq LLM (llama-3.3-70b-versatile)
    │
    ▼
Answer → Browser
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| 500-char chunk size | Balances context richness vs. retrieval precision |
| top_k = 3 chunks | Enough context without overloading the LLM prompt |
| MiniLM-L6-v2 | Fast, lightweight, runs locally — no API cost for embeddings |
| FAISS in-memory | Simple setup; resets on server restart (no persistence needed for demo) |
| Groq over OpenAI | Significantly faster inference, generous free tier |

---

## Limitations

- The FAISS index is **in-memory only** — restarting the server clears it, requiring re-upload
- Only one document is indexed at a time — uploading a new file replaces the previous index
- Chunk splitting is character-based, not sentence-aware — a chunk may cut mid-sentence
