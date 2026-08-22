# Knowledge Intelligence System

A document-based RAG application that lets users upload documents and ask natural-language questions about their content. The system retrieves relevant document chunks from ChromaDB and uses an OpenAI LLM to generate grounded answers.

## Features

- PDF, TXT, and Markdown document upload
- Document parsing, chunking, and OpenAI embeddings
- Semantic search with persistent ChromaDB
- RAG-based question answering with sources
- Conversation history for follow-up questions
- Duplicate document prevention using content-based IDs
- Document listing, deletion, and re-indexing
- Amazon S3 storage for original documents
- Pydantic request validation
- Dockerized deployment
- Pytest automated tests
- GitHub Actions CI/CD
- Automatic Docker image publishing to GHCR

## Architecture

```text
                    ┌───────────────┐
                    │     Web UI    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Flask API   │
                    └───────┬───────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Upload API     Document API     RAG Query
             │              │              │
             ▼              ▼              ▼
        Ingestion       Registry       Retrieval
             │              │              │
             ▼              │              ▼
        Embeddings          │          ChromaDB
             │              │              │
             └──────────────┘              ▼
                                      Relevant Chunks
                                            │
                                            ▼
                                        OpenAI LLM
                                            │
                                            ▼
                                         Answer

                       Original Documents
                              │
                              ▼
                           Amazon S3
```

## RAG Flow

```text
User Question
      ↓
Validation
      ↓
Query Transformation
      ↓
Query Embedding
      ↓
ChromaDB Similarity Search
      ↓
Similarity Filtering
      ↓
Relevant Context
      ↓
Conversation History
      ↓
OpenAI LLM
      ↓
Answer + Sources
```

The LLM is instructed to answer using the retrieved document context and avoid inventing information that is not present in the available context.

## Document Ingestion Flow

```text
Upload
  ↓
Validate File
  ↓
Generate Content-Based Document ID
  ↓
Check for Duplicate
  ↓
Upload Original to S3
  ↓
Parse Document
  ↓
Chunk Document
  ↓
Generate Embeddings
  ↓
Store Chunks in ChromaDB
  ↓
Register Metadata
```

## Tech Stack

- **Backend:** Python, Flask, Pydantic
- **AI/RAG:** OpenAI, LangChain
- **Embeddings:** OpenAI Embeddings
- **Vector Store:** ChromaDB
- **Object Storage:** Amazon S3
- **Testing:** Pytest
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Container Registry:** GitHub Container Registry

## Project Structure

```text
Knowledge-Intelligence-System/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── data/
│   ├── chroma/
│   ├── uploads/
│   └── documents.json
├── tests/
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
S3_BUCKET_NAME=your_bucket_name
```

**Never commit `.env` or API keys to GitHub.**

## Running Locally

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure `.env`, then start the application:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Running with Docker

Build:

```bash
docker build -t knowledge-intelligence-system .
```

Run:

```bash
docker run --env-file .env -p 5000:5000 -v "$(pwd)/data/chroma:/app/data/chroma" knowledge-intelligence-system
```

Open:

```text
http://127.0.0.1:5000
```

The ChromaDB directory is mounted to `/app/data/chroma`, allowing vector data to persist across container recreation.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/upload` | Upload and index a document |
| POST | `/query` | Ask a question about indexed documents |
| GET | `/documents` | List documents |
| GET | `/documents/<document_id>` | Get document metadata |
| DELETE | `/documents/<document_id>` | Delete a document |
| POST | `/documents/<document_id>/reindex` | Re-index a document |

Supported uploads: PDF, TXT, and Markdown.

## Document Identity and Idempotency

Documents receive a stable identifier derived from their file contents using SHA-256. Uploading the same document again is rejected instead of creating duplicate vector entries.

## Storage and Deletion

Original documents are stored in Amazon S3 while processed chunks are stored in ChromaDB.

When a document is deleted, the system removes its vector-store chunks, S3 object, and registry record.

If ingestion fails after an S3 upload, the system attempts to clean up the uploaded S3 object.

## Conversation History

Conversation history is maintained using a conversation ID and is included when generating responses. This enables follow-up questions within a conversation.

Very long conversations can increase token usage and may eventually approach the model's context limits.

## Testing

Run:

```bash
pytest
```

The automated test suite currently covers API model validation, configuration, and query transformation.

## CI/CD

Every push to `main` triggers GitHub Actions.

```text
Git Push
   ↓
Install Dependencies
   ↓
Run Tests
   ↓
Build Docker Image
   ↓
Publish Image to GHCR
```

The published image is:

```text
ghcr.io/pranjalchauhan404/knowledge-intelligence-system:latest
```

CI uses a dummy OpenAI key for tests; real API credentials are not stored in the repository.

## Current Status

Phase 7 hardening includes:

- API validation
- Error handling
- Document idempotency
- Document deletion and re-indexing
- Persistent ChromaDB
- Dockerization
- Automated tests
- GitHub Actions CI/CD
- Docker image publishing
- Reliability and performance review

The final end-to-end verification covers document upload, ingestion, retrieval, question answering, sources, conversation follow-ups, deletion, persistence after container restart, and CI/CD.
