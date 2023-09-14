from pydantic import BaseModel

from stats_copilot.types import ChatModel


class ChatRequest(BaseModel):
    model: ChatModel
    message: str
