from dependency_injector import containers, providers

from app.db.memory import LRUInMemoryDB
from app.services.chat import ChatService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".routers.chat",
        ]
    )
    db = providers.Singleton(LRUInMemoryDB)

    chat_service = providers.Factory(ChatService, db=db)
