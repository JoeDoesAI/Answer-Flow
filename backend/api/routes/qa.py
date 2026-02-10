from fastapi import Router

from api.deps import get_answer
retrieve_router = Router()

@retrieve_router.post('/generate_answer')
async def generate_answer(prompt:str,
                          vector_db,
                          get_answer:GenerationOchestrator = Depends(get_answer)):


    pass