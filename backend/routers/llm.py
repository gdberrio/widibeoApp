from fastapi import APIRouter, Form, Request

from stats_copilot.llm import chat

router = APIRouter(prefix="/v1/llm")


@router.post("/chat")
async def llm_chat(request: Request, model: str = Form(...), message: str = Form(...)):
    response = chat(model=model, user_message=message)
    return {"response": response}
