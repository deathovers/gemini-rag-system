import os
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.app.core.config import settings

class VectorStoreService:
    @staticmethod
    def get_embeddings():
        return GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

    @staticmethod
    def create_index(session_id: str, documents):
        embeddings = VectorStoreService.get_embeddings()
        vector_store = FAISS.from_documents(documents, embeddings)
        
        index_path = os.path.join(settings.STORAGE_DIR, session_id)
        vector_store.save_local(index_path)
        return vector_store

    @staticmethod
    def load_index(session_id: str):
        index_path = os.path.join(settings.STORAGE_DIR, session_id)
        if not os.path.exists(index_path):
            return None
        
        embeddings = VectorStoreService.get_embeddings()
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
