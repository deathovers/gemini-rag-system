import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class IngestionService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def process_pdf(self, file_path: str, filename: str) -> List[Document]:
        documents = []
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                metadata = {
                    "source": filename,
                    "page_number": page_num + 1
                }
                documents.append(Document(page_content=text, metadata=metadata))
        
        return self.text_splitter.split_documents(documents)
