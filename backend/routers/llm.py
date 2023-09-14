from fastapi import APIRouter

from stats_copilot.llm import chat
from stats_copilot import schemas

router = APIRouter(prefix="/v1/llm")


@router.post("/chat")
async def llm_chat(request: schemas.ChatRequest):
    model = request.model
    response = chat(model=model, user_message=request.message)
    return {"response": response}
