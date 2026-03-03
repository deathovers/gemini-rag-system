import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.app.core.config import settings

class VectorStoreService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def get_index_path(self, session_id: str):
        return os.path.join(settings.STORAGE_DIR, session_id)

    def create_or_update_index(self, session_id: str, documents):
        index_path = self.get_index_path(session_id)
        
        if os.path.exists(os.path.join(index_path, "index.faiss")):
            vectorstore = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
            vectorstore.add_documents(documents)
        else:
            vectorstore = FAISS.from_documents(documents, self.embeddings)
        
        vectorstore.save_local(index_path)

    def search(self, session_id: str, query: str, k: int = 5):
        index_path = self.get_index_path(session_id)
        if not os.path.exists(index_path):
            return []
        
        vectorstore = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        return vectorstore.similarity_search(query, k=k)
