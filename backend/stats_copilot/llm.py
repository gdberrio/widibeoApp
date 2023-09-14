import os
from dotenv import load_dotenv
import openai
from stats_copilot.types import ChatModel

load_dotenv()


def chat(model: ChatModel, user_message: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": user_message}]
    )

    return completion.choices[0].message.content
