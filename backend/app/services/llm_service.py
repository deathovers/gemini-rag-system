from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from backend.app.core.config import settings

class LLMService:
    def __init__(self):
        # Using gemini-3-flash as per user feedback
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    async def get_response(self, query: str, context: str):
        system_prompt = (
            "You are a helpful assistant for document-based Q&A. "
            "Use the following pieces of retrieved context to answer the question. "
            "If the answer is not contained within the provided context, state: "
            "'The answer was not found in the uploaded documents.' "
            "Do not use external knowledge. Provide citations if possible.\n\n"
            "Context:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{query}"),
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"context": context, "query": query})
        return response.content
