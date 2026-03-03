# DocuChat AI Backend

FastAPI-based RAG system using Google Gemini and FAISS.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example` and add your `GOOGLE_API_KEY`.

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `POST /api/upload`: Upload PDF files. Returns a `session_id`.
- `POST /api/query`: Query the uploaded documents using a `session_id`.
