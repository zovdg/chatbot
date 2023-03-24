import logging

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dependency_injector.wiring import inject, Provide

from app.services.chat import ChatService
from app.container import Container

LOG = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
@inject
async def home(
    request: Request,
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    # use client ip as chat_id.
    chat_id = request.client.host
    LOG.debug(f"client: {chat_id} coming...")

    contexts = chat_service.greetings(chat_id)
    return templates.TemplateResponse(
        "chats.html", {"request": request, "contexts": [c.dict() for c in contexts]}
    )


@router.post("/", response_class=HTMLResponse)
@inject
def chats(
    request: Request,
    cmd: str = Form(...),
    message: str = Form(None),
    history: str = Form("[]"),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    # use client ip as chat_id.
    chat_id = request.client.host
    LOG.debug(f"client: {chat_id} chats...")

    if cmd == "clear":
        chat_service.clear(chat_id=chat_id)
        contexts = chat_service.greetings(chat_id)
    else:
        contexts = chat_service.chat(chat_id=chat_id, message=message)
    return templates.TemplateResponse(
        "chats.html",
        context={"request": request, "contexts": [c.dict() for c in contexts]},
    )
