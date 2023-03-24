import openai

from app.config import settings


openai.api_key = settings.openai_api_key


def chat_completion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model=settings.openai_model,
        temperature=0.5,
        presence_penalty=0,
        frequency_penalty=0,
        messages=[
            {
                "role": "system",
                "content": f"{impersonated_role}. Conversation history: {chat_history}",
            },
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ],
    )

    chatgpt_output = None
    for item in output["choices"]:
        chatgpt_output = item["message"]["content"]

    return chatgpt_output
