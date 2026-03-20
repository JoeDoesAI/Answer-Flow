from fastapi import APIRouter, Request,Depends
from fastapi.responses import StreamingResponse
from schemas.qa import QA_Response
from services.qa.ochestrator import RetrivalOchestrator

from api.deps.service_deps import get_query_ans
qa_router = APIRouter()

@qa_router.post("/query",response_model=QA_Response)
async def answer_prompt(request:Request,
                        user_query: str,
                        answer:RetrivalOchestrator = Depends(get_query_ans)):
    
    generator = answer.run(user_query)

    return StreamingResponse(generator, media_type="text/plain")


