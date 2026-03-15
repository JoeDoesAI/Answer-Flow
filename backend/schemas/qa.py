from pydantic import BaseModel

class QA_Response(BaseModel):
    prompt_response: str
    citation: str