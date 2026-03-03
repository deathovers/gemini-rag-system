from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from backend.app.services.vector_store import VectorStoreService
from backend.app.core.config import settings

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    async def get_response(self, session_id: str, query: str):
        vector_store = VectorStoreService.load_index(session_id)
        if not vector_store:
            return "No documents found for this session. Please upload PDFs first.", []

        # Retrieve top K chunks
        docs = vector_store.similarity_search(query, k=5)
        
        # Format context with structured metadata for the LLM
        context_parts = []
        sources = []
        seen_sources = set()
        
        for doc in docs:
            doc_name = doc.metadata.get("source", "Unknown")
            page_num = doc.metadata.get("page", 0) + 1
            
            source_key = f"{doc_name}-{page_num}"
            if source_key not in seen_sources:
                sources.append({"document": doc_name, "page": page_num})
                seen_sources.add(source_key)
            
            # Injecting metadata into the context string for the LLM to fulfill citation requirement
            context_parts.append(
                f"[Document: {doc_name}, Page: {page_num}]\n{doc.page_content}"
            )

        context_text = "\n\n".join(context_parts)

        template = """
        You are a helpful AI assistant. Answer the question based ONLY on the provided context.
        If the answer is not contained within the context, state: 'The answer was not found in the uploaded documents.'
        Do not use external knowledge.

        Context:
        {context}

        Question: {query}

        Instructions: Provide a detailed answer. You MUST cite the source document and page number for the information you provide.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm
        
        response = await chain.ainvoke({"context": context_text, "query": query})
        
        return response.content, sources
