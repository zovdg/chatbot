import openai

from app.config import settings
from app import models

openai.api_key = settings.openai_api_key


def chat_completion(
    user_input: str,
    chat: models.Chat,
    model: str = settings.openai_model,
    temperature: float = settings.openai_temperature,
) -> models.Chat:
    # user input.
    chat.user_said(message=user_input)

    # request ChatGPT.
    output = openai.ChatCompletion.create(
        model=model,
        messages=chat.messages,
        temperature=temperature,
    )

    # assistant output.
    content = output["choices"][0]["message"]["content"]
    chat.assistant_said(message=content)

    # back new chats.
    return chat
