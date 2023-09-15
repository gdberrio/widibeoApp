from pydantic import BaseModel

from stats_copilot.llm import ChatModel


class ChatRequest(BaseModel):
    model: ChatModel
    message: str
