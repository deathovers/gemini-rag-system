from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.services.vector_store import load_vector_store
from app.core.config import settings

def get_rag_response(session_id: str, query: str):
    vector_store = load_vector_store(session_id)
    if not vector_store:
        return "No documents uploaded for this session.", []
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY)
    
    template = """
    You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
    If the answer is not contained within the provided context, state: 'The answer was not found in the uploaded documents.' 
    Do not use external knowledge.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    result = qa_chain({"query": query})
    
    answer = result["result"]
    source_docs = result["source_documents"]
    
    sources = []
    for doc in source_docs:
        sources.append({
            "document": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", 0) + 1
        })
    
    unique_sources = []
    seen = set()
    for s in sources:
        identifier = f"{s['document']}-{s['page']}"
        if identifier not in seen:
            unique_sources.append(s)
            seen.add(identifier)
            
    return answer, unique_sources
