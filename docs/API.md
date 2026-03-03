# API Documentation - DocuChat AI

The DocuChat AI backend is built with FastAPI and provides endpoints for document management and querying.

## Base URL
`http://localhost:8000`

---

## Endpoints

### 1. Upload Documents
**Endpoint:** `POST /upload`  
**Description:** Uploads one or more PDF files to initialize or update a session.

**Request:**
- **Type:** `multipart/form-data`
- **Body:**
    - `files`: List of PDF files.
    - `session_id` (Optional): A UUID string. If not provided, a new one is generated.

**Response:**
```json
{
  "session_id": "uuid-string",
  "files": [
    {
      "filename": "contract.pdf",
      "status": "processed"
    }
  ]
}
```

### 2. Query Documents
**Endpoint:** `POST /query`  
**Description:** Ask a question based on the documents uploaded in a specific session.

**Request Body:**
```json
{
  "session_id": "uuid-string",
  "query": "What is the termination clause in the contract?"
}
```

**Response:**
```json
{
  "answer": "The termination clause states that either party can terminate with 30 days notice (Source: contract.pdf, Page: 5).",
  "sources": [
    {
      "document": "contract.pdf",
      "page": 5
    }
  ]
}
```

### 3. Delete Document (Planned)
**Endpoint:** `DELETE /document/{file_id}`  
**Description:** Removes a specific document from the session and updates the vector index.

---

## Error Handling

| Code | Description |
|------|-------------|
| 400  | Bad Request (e.g., non-PDF file uploaded). |
| 404  | Session not found or no documents uploaded for session. |
| 500  | Internal Server Error (e.g., LLM API failure). |

## Security & Isolation
- Data is isolated by `session_id`. 
- FAISS indices are stored locally and mapped to specific sessions.
- Ensure `session_id` is kept secure on the client side.
