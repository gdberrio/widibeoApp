import os
from dotenv import load_dotenv
import openai

from typing import Literal

load_dotenv()

OpenAIModel = Literal["gpt-3.5-turbo"] | Literal["gpt-3.5-turbo-16k"] | Literal["gpt-4"]

ChatModel = OpenAIModel


def chat(model: ChatModel, user_message: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": user_message}]
    )

    return completion.choices[0].message.content
