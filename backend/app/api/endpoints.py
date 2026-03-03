import uuid
import tempfile
import shutil
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.models.schemas import QueryRequest, QueryResponse, UploadResponse, Source
from app.services.ingestion import process_pdfs
from app.services.llm_service import get_rag_response

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...), session_id: str = Form(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    
    temp_files = []
    filenames = []
    
    try:
        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                continue
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            shutil.copyfileobj(file.file, temp_file)
            temp_file.close()
            temp_files.append(temp_file)
            filenames.append(file.filename)
        
        if not temp_files:
            raise HTTPException(status_code=400, detail="No valid PDF files uploaded.")
            
        processed_files = process_pdfs(temp_files, filenames, session_id)
        
    finally:
        for temp_file in temp_files:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
                
    return UploadResponse(session_id=session_id, files=processed_files)

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    answer, sources = get_rag_response(request.session_id, request.query)
    
    formatted_sources = [Source(document=s["document"], page=s["page"]) for s in sources]
    
    return QueryResponse(answer=answer, sources=formatted_sources)
