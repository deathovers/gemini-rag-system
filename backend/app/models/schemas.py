from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    session_id: str
    query: str

class SourceMetadata(BaseModel):
    document: str
    page: int

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceMetadata]

class UploadResponse(BaseModel):
    session_id: str
    files: List[str]
    status: str
