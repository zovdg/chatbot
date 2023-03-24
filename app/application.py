import logging

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

from app.container import Container
from app.routers import chat

LOG = logging.getLogger(__name__)

# templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    container = Container()
    web = FastAPI()
    web.container = container
    web.include_router(chat.router)
    return web


app = create_app()
app.mount("/static", StaticFiles(directory="static"), name="static")
