# Customer Support Assistant

## Overview

A Django-based Retrieval-Augmented Generation (RAG) system for intelligent customer support using local LLMs and vector embeddings.

## Features

- **Document Ingestion**: Upload and process PDF/TXT documents
- **Vector Search**: FAISS-based semantic search with embeddings
- **Local LLM**: Gemma 3.1B for offline answer generation
- **REST API**: Query endpoint for programmatic access
- **Web Dashboard**: Interactive chat interface

## Tech Stack

- Django 4.2 + Django REST Framework
- FAISS for vector indexing
- Sentence Transformers for embeddings
- Hugging Face Transformers (Gemma)
- MySQL database

## Quick Start

1. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Configure database** in `settings.py`

3. **Run migrations**

    ```bash
    python manage.py migrate
    ```

4. **Upload documents**
    - Navigate to `/upload/` and select files

5. **Query the system**
    - Use `/dashboard/` for chat
    - Or POST to `/query/` API endpoint

## Project Structure

```txt
customer_support/
├── knowledge/          # Core RAG application
│   ├── models.py
│   ├── query_service.py
│   ├── embedding_service.py
│   ├── llm_service.py
│   └── vector_index.py
├── settings.py
└── urls.py
```

## Configuration

- Embedding model: `all-MiniLM-L6-v2` (384-dim)
- LLM model: `google/gemma-3-1b-it`
- Default top-k retrieval: 5 chunks
