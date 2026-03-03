import uuid
import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.models.schemas import QueryRequest, QueryResponse, UploadResponse
from backend.app.services.ingestion import IngestionService
from backend.app.services.vector_store import VectorStoreService
from backend.app.services.llm_service import LLMService
from backend.app.core.config import settings

app = FastAPI(title="DocuChat AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()

@app.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    session_id = str(uuid.uuid4())
    temp_dir = os.path.join(settings.STORAGE_DIR, "temp", session_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    all_chunks = []
    uploaded_filenames = []
    
    try:
        for file in files:
            if not file.filename.endswith(".pdf"):
                continue
                
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            chunks = IngestionService.process_pdf(file_path, file.filename)
            all_chunks.extend(chunks)
            uploaded_filenames.append(file.filename)
            
        if not all_chunks:
            raise HTTPException(status_code=400, detail="No valid PDF files uploaded.")
            
        VectorStoreService.create_index(session_id, all_chunks)
        
        return UploadResponse(
            session_id=session_id,
            files=uploaded_filenames,
            status="processed"
        )
    finally:
        # Cleanup temp files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    answer, sources = await llm_service.get_response(request.session_id, request.query)
    return QueryResponse(answer=answer, sources=sources)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
