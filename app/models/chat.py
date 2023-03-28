from enum import Enum
from pydantic import BaseModel, Field

from app import utils
from app.config import settings


class Role(Enum):
    System: str = "system"
    User: str = "user"
    Assistant: str = "assistant"


class Message(BaseModel):
    role: Role
    content: str = Field(..., min_length=1)
    time: str = Field(default_factory=utils.current_time)

    @classmethod
    def system(cls):
        return cls(role=Role.System, content="You are a helpful assistant.")

    @classmethod
    def user(cls, content: str):
        return cls(role=Role.User, content=content)

    @classmethod
    def assistant(cls, content: str):
        return cls(role=Role.Assistant, content=content)

    def to_message(self):
        return {
            "role": self.role.value,
            "content": self.content,
        }

    def to_chat(self):
        return {
            "role": self.role.value,
            "content": self.content,
            "time": self.time
        }


class Chat:
    def __init__(self):
        self._messages = [Message.system()]

    def user_said(self, message: str):
        self._messages.append(Message.user(content=message))

    def assistant_said(self, message: str):
        self._messages.append(Message.assistant(content=message))

    @property
    def messages(self):
        return [msg.to_message() for msg in self._messages]

    @property
    def chats(self):
        chats = [Message.assistant("What can I help you?")]
        for message in self._messages[1:]:
            chats.append(message)
        return [c.to_chat() for c in chats]
