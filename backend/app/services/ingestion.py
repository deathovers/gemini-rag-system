import os
import tempfile
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.vector_store import save_vector_store, load_vector_store, get_embeddings
from langchain_community.vectorstores import FAISS

def process_pdfs(files: List[tempfile.NamedTemporaryFile], filenames: List[str], session_id: str):
    all_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    for file, filename in zip(files, filenames):
        loader = PyMuPDFLoader(file.name)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = filename
        
        split_docs = text_splitter.split_documents(docs)
        all_docs.extend(split_docs)
    
    embeddings = get_embeddings()
    
    existing_store = load_vector_store(session_id)
    if existing_store:
        existing_store.add_documents(all_docs)
        save_vector_store(existing_store, session_id)
    else:
        vector_store = FAISS.from_documents(all_docs, embeddings)
        save_vector_store(vector_store, session_id)
    
    return filenames
