import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.app.core.config import settings

class IngestionService:
    @staticmethod
    def process_pdf(file_path: str, filename: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Update metadata to ensure filename is correct
        for doc in documents:
            doc.metadata["source"] = filename
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents)
        return chunks
