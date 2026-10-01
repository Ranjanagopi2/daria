# Engineering Mechanics RAG Agent

A Retrieval-Augmented Generation (RAG) subsystem developed as part of a larger LangGraph-based Research & Summarization Agent project.

The goal of this component is to provide reliable, source-grounded retrieval from an Engineering Mechanics textbook using Docling, ChromaDB, and semantic search with reranking.

---

## Overview

This RAG pipeline converts a textbook into a structured knowledge base and retrieves relevant evidence for user queries.

### Pipeline

```text
Engineering Mechanics PDF
            ↓
         Docling
            ↓
    Knowledge Objects
            ↓
 knowledge_objects.pkl
            ↓
      BGE Embeddings
            ↓
        ChromaDB
            ↓
     Semantic Search
            ↓
 Cross-Encoder Reranking
            ↓
     Evidence Package
```

---

## Corpus

**Book:** Engineering Mechanics: Statics

The corpus was selected to align with the long-term objective of applying AI and Agentic Systems to Mechanical Engineering education and problem-solving.

---

## Features

### Document Processing

* PDF ingestion using Docling
* Structured content extraction
* Hierarchical metadata extraction
* Knowledge object generation
* Persistent intermediate artifacts

### Metadata Captured

```python
{
    "chapter",
    "section",
    "subsection",
    "page",
    "source_file",
    "content_type"
}
```

### Vector Database

* Embedding Model: `BAAI/bge-small-en-v1.5`
* Vector Store: ChromaDB
* Persistent storage
* Rebuildable from knowledge objects

### Retrieval

* Semantic retrieval using ChromaDB
* Initial retrieval: Top 10 candidates
* Cross-encoder reranking
* Final evidence: Top 3 passages

### Reranker

Model:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Retrieval Pipeline:

```text
Query
 ↓
BGE Embedding
 ↓
Chroma Top 10
 ↓
Cross Encoder
 ↓
Top 3 Evidence
```

---

## Project Structure

```text
rag/

├── data/
│
├── outputs/
│   ├── knowledge_objects.pkl
│   └── chroma_db/
│
├── ingestion/
│   ├── extract_docling.py
│   └── create_knowledge_objects.py
│
├── vectorstore/
│   ├── build_vector_db.py
│   └── verify_vector_db.py
│
├── retrieval/
│   ├── retrieve.py
│   ├── rerank.py
│   └── rag_agent.py
│
├── evaluation/
│   └── test_queries.py
│
└── config.py
```

---

## Build Vector Database

```bash
python -m rag.vectorstore.build_vector_db
```

This script:

* Loads `knowledge_objects.pkl`
* Generates embeddings
* Creates ChromaDB collection
* Stores documents and metadata

---

## Verify Retrieval

```bash
python -m rag.vectorstore.verify_vector_db
```

Validation queries include:

* What is statics?
* What is Newton's First Law?
* What is torque?
* What is a scalar quantity?

---

## Usage

```python
from rag.retrieval.rag_agent import search

result = search(
    "What is Newton's First Law?"
)
```

Example output:

```python
{
    "query": "...",

    "retrieval_metadata": {
        "initial_candidates": 10,
        "final_evidence": 3,
        "retrieval_method":
            "bge+chroma+cross_encoder"
    },

    "evidence": [...],

    "sources": [...]
}
```

---

## Results

Final Indexed Documents:

```text
1614
```

Retrieval stack:

```text
Docling
+
BGE Embeddings
+
ChromaDB
+
Cross Encoder Reranking
```

The reranking layer significantly improved retrieval quality for concept-specific engineering queries by promoting highly relevant passages over semantically similar but less precise matches.

---

## Future Enhancements

* Multimodal retrieval
* Figure-aware retrieval
* Equation-aware retrieval
* Example-aware retrieval
* Multi-book engineering knowledge base
* Engineering problem-solving agent
* Tutor mode with guided derivations
* Hybrid retrieval strategies

---

## Status

```text
RAG SUBSYSTEM STATUS: FROZEN
```

Completed:

✓ Docling Extraction
✓ Knowledge Objects
✓ Hierarchical Metadata
✓ BGE Embeddings
✓ ChromaDB
✓ Semantic Retrieval
✓ Cross-Encoder Reranking
✓ RAG Agent API
