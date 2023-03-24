import logging

from typing import Optional, List

from app.config import settings
from app.openai.client import ask_chat_gpt

from app.db.base import DB
from app.db.memory import InMemoryDB

from app import models

LOG = logging.getLogger(__name__)


class ChatService:
    def __init__(self, db: DB = None):
        self.db = db or InMemoryDB()

    def greetings(self, chat_id: str) -> List[models.Chat]:
        self.db.set(key=chat_id, value=[])
        contexts = self.db.get(key=chat_id)
        contexts.append(models.Chat.chat_gpt_speak("What can I help you?"))
        return contexts

    def chat(self, chat_id: str, message: Optional[str] = None) -> List[models.Chat]:
        if not self.db.exist(chat_id):
            self.db.set(key=chat_id, value=[])

        contexts = self.db.get(chat_id)
        if not message:
            LOG.warning("Human said nothing...")
            return contexts

        if settings.debug:
            output = "...debug..."
        else:
            output = ask_chat_gpt(question=message, contexts=contexts)

        contexts.append(models.Chat.human_speak(message))
        contexts.append(models.Chat.chat_gpt_speak(output))
        return contexts

    def clear(self, chat_id: str):
        self.db.delete(chat_id)
