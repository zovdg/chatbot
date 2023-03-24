import logging
import json

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dependency_injector.wiring import inject, Provide

from app import utils

from app.openai.client import chat_completion
from app.config import settings
from app.services.chat import ChatService
from app.container import Container
from app.routers import chat

LOG = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    container = Container()
    web = FastAPI()
    web.container = container
    web.include_router(chat.router)
    return web


app = create_app()
app.mount("/static", StaticFiles(directory="static"), name="static")
