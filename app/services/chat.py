import logging

from typing import Optional, List, Dict

from app.config import settings
from app.openai.client import chat_completion

from app.db.base import DB
from app.db.memory import InMemoryDB

from app import models

LOG = logging.getLogger(__name__)


class ChatService:
    def __init__(self, db: DB = None):
        self.db = db or InMemoryDB()

    def greetings(self, chat_id: str) -> List[Dict]:
        if not self.db.exist(chat_id):
            self.db.set(key=chat_id, value=models.Chat())
        chat = self.db.get(key=chat_id)
        return chat.chats

    def chat(self, chat_id: str, message: Optional[str] = None) -> List[Dict]:
        if not self.db.exist(chat_id):
            self.db.set(key=chat_id, value=[])

        chat = self.db.get(chat_id)
        if not message:
            LOG.warning("Human said nothing...")
            return chat.chats

        if settings.fake_ask:
            chat.user_said(message)
            chat.assistant_said("...debug...")
        else:
            chat_completion(user_input=message, chat=chat)

        return chat.chats

    def clear(self, chat_id: str):
        self.db.delete(chat_id)
