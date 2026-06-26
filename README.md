# RAG Studio

A production-grade Retrieval-Augmented Generation application with built-in cost optimization techniques, built on FastAPI + React.

## Architecture

```
rag-app/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/routes/       # documents.py · query.py · system.py
│   │   ├── core/             # config · logging · exceptions
│   │   ├── middlewares/      # global error handler
│   │   ├── models/           # domain.py (dataclasses) · schemas.py (Pydantic)
│   │   └── services/
│   │       ├── chunking/     
│   │       ├── embedding/    # embedding_service (Groq nomic-embed-text)
│   │       ├── vector_store/ # in-memory cosine similarity store
│   │       ├── cache/        # semantic_cache
│   │       ├── rag/          # rag_pipeline · query_compressor · context_builder · factory
│   │       └── document_service.py
│   ├── main.py
│   └── requirements.txt
└── frontend/                 # React + Vite + Tailwind
    └── src/
        ├── components/
        │   ├── features/     
        │   │                 
        │   ├── layout/       
        │   └── ui/           
        ├── hooks/            
        ├── services/         
        ├── store/            
        └── types/            
```

## Cost Optimization Techniques

| Technique | Description | Typical Savings |
|---|---|---|
| **Semantic Cache** | Embeds every query; skips the LLM entirely if a sufficiently similar query was answered recently (cosine ≥ 0.92) | 100% on cache hits |
| **Query Compression** | Rewrites verbose questions into concise keyword queries, reducing prompt tokens | ~15% |
| **Token-Budget Context** | Ranks retrieved chunks and trims context to a configurable token ceiling | ~10–25% |
| **Sentence-Aware Chunking** | Splits on sentence boundaries with overlap, avoiding wasted tokens from mid-sentence cuts | Indirect |
| **Batched Embeddings** | Sends up to 96 texts per embedding API call | Reduces latency & rate-limit risk |
| **Smallest Capable Model** | Uses `llama3-8b-8192` by default — fast and cheap for RAG tasks | vs. larger models |

## Quickstart

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and set GROQ_API_KEY

python main.py
# → http://localhost:8000
# → Swagger UI at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

## API Reference

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/documents` | Upload a document (multipart/form-data) |
| `GET` | `/api/v1/documents` | List all documents |
| `GET` | `/api/v1/documents/{id}` | Get document by ID |
| `DELETE` | `/api/v1/documents/{id}` | Delete document and its vectors |
| `POST` | `/api/v1/query` | Run a RAG query |
| `GET` | `/cache/stats` | Semantic cache hit/miss stats |
| `DELETE` | `/cache` | Clear semantic cache |
| `GET` | `/health` | Health check |

### Query Request

```json
{
  "question": "What is the main conclusion of the paper?",
  "document_id": "optional-uuid-to-scope-to-one-doc",
  "top_k": 4
}
```

### Query Response

```json
{
  "answer": "The main conclusion is...",
  "sources": [{ "chunk_id": "...", "text": "...", "score": 0.91, "chunk_index": 3 }],
  "cost_metrics": {
    "prompt_tokens": 812,
    "completion_tokens": 134,
    "total_tokens": 946,
    "cache_hit": false,
    "chunks_retrieved": 3,
    "query_compressed": true,
    "estimated_savings_pct": 22.5
  },
  "cached": false
}
```

## Supported File Types

- PDF (`.pdf`)
- Word (`.docx`)
- Plain text (`.txt`)
- Markdown (`.md`)
- Max size: 20 MB

## Configuration

All knobs live in `.env` (see `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | Required |
| `LLM_MODEL` | `llama3-8b-8192` | Groq LLM model |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Groq embedding model |
| `CHUNK_SIZE` | `512` | Target tokens per chunk |
| `CHUNK_OVERLAP` | `64` | Overlap tokens between chunks |
| `MAX_RETRIEVED_CHUNKS` | `4` | Max chunks sent to LLM |
| `MAX_CONTEXT_TOKENS` | `3000` | Hard token ceiling for context |
| `SEMANTIC_CACHE_TTL_SECONDS` | `3600` | Cache entry lifetime |
| `SEMANTIC_CACHE_SIMILARITY_THRESHOLD` | `0.92` | Cosine threshold for cache hit |
| `QUERY_COMPRESSION_ENABLED` | `true` | Toggle query compression |
