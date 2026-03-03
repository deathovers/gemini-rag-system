# DocuChat AI

DocuChat AI is a professional Multi-Document RAG (Retrieval-Augmented Generation) assistant. It allows users to upload multiple PDF documents and interact with them using an AI powered by Google Gemini. The system ensures strict data isolation through session-based vector indexing and provides verifiable citations for every answer.

## 🚀 Features

- **Multi-Document Support:** Upload and query multiple PDFs simultaneously.
- **Session Isolation:** Each user session has its own private FAISS vector index.
- **Source-Backed Citations:** Every response includes the document name and page number.
- **Strict Grounding:** The AI is instructed to only answer based on the provided documents.
- **High Performance:** Powered by Google Gemini 1.5 Flash for fast reasoning and Gemini Embeddings for accurate retrieval.

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **LLM:** Google Gemini 1.5 Flash
- **Embeddings:** Google Gemini Embedding Model (`models/embedding-001`)
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **Orchestration:** LangChain
- **PDF Processing:** PyPDFLoader

## 📋 Prerequisites

- Python 3.9+
- Google Cloud API Key (with Gemini API access)

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/docuchat-ai.git
   cd docuchat-ai
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the `backend` directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   EMBEDDING_MODEL=models/embedding-001
   ```

## 🏃 Usage

1. **Start the Backend Server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Access the API:**
   The API will be available at `http://localhost:8000`.
   You can view the interactive Swagger documentation at `http://localhost:8000/docs`.

## 🏗️ Architecture

1. **Ingestion:** PDFs are uploaded, parsed by `PyPDFLoader`, and split into chunks using `RecursiveCharacterTextSplitter`.
2. **Indexing:** Chunks are converted into embeddings via Gemini and stored in a session-specific FAISS index.
3. **Retrieval:** When a query is made, the system performs a similarity search in the session's FAISS index.
4. **Generation:** The top-K chunks are injected into a prompt with metadata (source/page). Gemini 1.5 Flash generates a response based *only* on that context.
