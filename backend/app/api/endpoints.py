import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from backend.app.models.schemas import QueryRequest, QueryResponse, UploadResponse, Source
from backend.app.services.ingestion import IngestionService
from backend.app.services.vector_store import VectorStoreService
from backend.app.services.llm_service import LLMService
from backend.app.core.config import settings

router = APIRouter()
ingestion_service = IngestionService()
vector_store_service = VectorStoreService()
llm_service = LLMService()

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...), session_id: str = None):
    if not session_id:
        session_id = str(uuid.uuid4())
    
    session_dir = os.path.join(settings.STORAGE_DIR, f"tmp_{session_id}")
    os.makedirs(session_dir, exist_ok=True)
    
    filenames = []
    all_chunks = []
    
    for file in files:
        if not file.filename.endswith(".pdf"):
            continue
            
        file_path = os.path.join(session_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        chunks = ingestion_service.process_pdf(file_path, file.filename)
        all_chunks.extend(chunks)
        filenames.append(file.filename)
    
    if all_chunks:
        vector_store_service.create_or_update_index(session_id, all_chunks)
    
    # Cleanup temp files
    shutil.rmtree(session_dir)
    
    return UploadResponse(session_id=session_id, filenames=filenames, status="processed")

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    relevant_docs = vector_store_service.search(request.session_id, request.query)
    
    if not relevant_docs:
        return QueryResponse(
            answer="No documents found for this session. Please upload PDFs first.",
            sources=[]
        )
    
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    answer = await llm_service.get_response(request.query, context)
    
    sources = []
    seen_sources = set()
    for doc in relevant_docs:
        src_key = f"{doc.metadata['source']}_{doc.metadata['page_number']}"
        if src_key not in seen_sources:
            sources.append(Source(document=doc.metadata['source'], page=doc.metadata['page_number']))
            seen_sources.add(src_key)
            
    return QueryResponse(answer=answer, sources=sources)
