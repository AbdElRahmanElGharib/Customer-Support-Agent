# Customer Support Knowledge Agent (POC)

## Purpose

- Build a backend system that integrates ML into a production-style Django stack
- Focus on system design, async processing, caching, and clean ML integration
- Proof of concept, not a production product

---

## Problem

- Customer support knowledge (FAQs, policies, past tickets) is hard to query efficiently
- Need a system to ingest, index, and retrieve this knowledge using similarity search

---

## Core Features

- Upload support knowledge (documents / tickets)
- Asynchronous processing and indexing
- Vector-based similarity search
- Cached query results
- Traceable query execution
- Optional local LLM-based answer generation

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework (DRF)
- MySQL (single source of truth)

### Async & Infrastructure

- Celery (background tasks)
- Redis (broker, result backend, cache)
- Bash (local scripts)

### Machine Learning (Local Only)

- Sentence embeddings (local model)
- Vector store (FAISS or equivalent local store)
- Cosine similarity / Top-K retrieval
- Optional small local LLM (no external APIs)

---

## High-Level Flow

- Upload data → store metadata → trigger async task
- Celery chunks text → generates embeddings → stores vectors
- Query arrives → cache lookup → similarity search
- Retrieved context returned (or passed to local LLM)
- Query trace stored in DB

---

## Project Phases

1. Project framing and constraints
2. Git flow and conventional commits
3. Backend skeleton
4. Data modeling
5. Upload API
6. Async ingestion pipeline
7. Vector search
8. Caching
9. Query API (end-to-end)
10. Observability and traceability
11. Final documentation

---

## Non-Goals

- No frontend UI
- No online ML services
- No model training or fine-tuning
- No autonomous agents or chains
- No premature optimization

---

## Success Criteria

- Runs locally
- Async tasks work independently
- Cache hits observable
- Similarity search returns relevant results
- Queries are explainable and traceable
- ML code is isolated and deterministic
