from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    session_id: str
    query: str

class Source(BaseModel):
    document: str
    page: int

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]

class UploadResponse(BaseModel):
    session_id: str
    filenames: List[str]
    status: str
