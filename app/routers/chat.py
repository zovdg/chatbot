import logging

from typing import Optional

from fastapi import APIRouter, Request, Form, Depends, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dependency_injector.wiring import inject, Provide

from app.services.chat import ChatService
from app.container import Container
from app import utils

LOG = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


async def set_cookie(response: Response, chat_id: Optional[str] = None):
    chat_id = chat_id or utils.new_chat_id()
    LOG.debug(f"Set cookie, chat_id: {chat_id}")
    response.set_cookie(key="chat_id", value=chat_id)


@router.get("/", response_class=HTMLResponse)
@inject
async def home(
    request: Request,
    chat_id: Optional[str] = Cookie(None),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    # use client ip as chat_id.
    # chat_id = request.client.host
    should_set_cookie = False if chat_id else True

    # get cookie chat_id or new one.
    chat_id = chat_id or utils.new_chat_id()

    LOG.debug(f"client {request.client.host}, with chat id: {chat_id} coming...")

    contexts = chat_service.greetings(chat_id)
    response = templates.TemplateResponse(
        "chats.html", {"request": request, "contexts": [c.dict() for c in contexts]}
    )
    if should_set_cookie:
        await set_cookie(response, chat_id)
    return response


@router.post("/", response_class=HTMLResponse)
@inject
def chats(
    request: Request,
    cmd: str = Form(...),
    message: str = Form(None),
    history: str = Form("[]"),
    chat_id: Optional[str] = Cookie(None),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
):
    # use client ip as chat_id.
    # chat_id = request.client.host
    LOG.debug(f"client {request.client.host}, with chat id: {chat_id} chats...")

    if cmd == "clear":
        chat_service.clear(chat_id=chat_id)
        contexts = chat_service.greetings(chat_id)
    else:
        contexts = chat_service.chat(chat_id=chat_id, message=message)
    return templates.TemplateResponse(
        "chats.html",
        context={"request": request, "contexts": [c.dict() for c in contexts]},
    )
