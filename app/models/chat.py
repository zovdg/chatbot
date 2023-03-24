from enum import Enum
from pydantic import BaseModel, Field

from app import utils


class Role(str, Enum):
    ChatGPT = "ChatGPT"
    Human = "Human"


class Chat(BaseModel):
    role: Role
    message: str
    time: str = Field(default_factory=utils.current_time)

    @classmethod
    def human_speak(cls, message: str):
        return cls(role=Role.Human, message=message)

    @classmethod
    def chat_gpt_speak(cls, message: str):
        return cls(role=Role.ChatGPT, message=message)
