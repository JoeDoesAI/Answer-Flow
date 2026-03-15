from ingestion_service.store_vectors import VectorDB
from embedding_service.generate_embedding import GenerateEmbeddings
from qa.llm_generation import LLMService


from typing import AsyncGenerator

class RetrivalOchestrator():
    def __init__(self, convert_vector:GenerateEmbeddings, search_vector:VectorDB, llm_service:LLMService):
        self.convert_vector = convert_vector
        self.search_vector = search_vector
        self.llm_service = llm_service

    async def run(self,user_query) -> AsyncGenerator[str, None]:
        prompt_embedding = self.convert_vector(user_query)

        context = self.search_vector.search_vectors(prompt_embedding)

        full_prompt = f"{context}{user_query}"

        async for token in self.llm_service.groq_stream_generator(full_prompt):
            yield token


