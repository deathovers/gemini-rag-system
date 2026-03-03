import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_API_KEY)

def get_index_path(session_id: str):
    path = os.path.join(settings.STORAGE_DIR, session_id)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def save_vector_store(vector_store: FAISS, session_id: str):
    path = get_index_path(session_id)
    vector_store.save_local(path)

def load_vector_store(session_id: str):
    path = get_index_path(session_id)
    if os.path.exists(os.path.join(path, "index.faiss")):
        return FAISS.load_local(path, get_embeddings(), allow_dangerous_deserialization=True)
    return None
