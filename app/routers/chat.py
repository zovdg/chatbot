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
        """
        contexts = json.loads(history)
        if message:
            if settings.debug:
                chatgpt_raw_output = "xxxxxxxxxxxxxx\nxxxxxxxxxxxxx"
            else:
                chatgpt_raw_output = chat_completion(
                    user_input=message,
                    impersonated_role="",
                    explicit_input="",
                    chat_history="",
                )

            contexts.append(
                {
                    "message": message.replace("\n", "<br>"),
                    "is_bot": False,
                    "time": utils.current_time(),
                }
            )
            contexts.append(
                {
                    "message": chatgpt_raw_output.replace("\n", "<br>"),
                    "is_bot": True,
                    "time": utils.current_time(),
                }
            )
        """
    # history = json.dumps(contexts)
    return templates.TemplateResponse(
        "chats.html",
        context={"request": request, "contexts": [c.dict() for c in contexts]},
    )
