import json
import pytz

from datetime import datetime

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.openai.client import chat_completion

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def current_time():
    tz_sh = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz=tz_sh)
    return now.strftime("%Y/%m/%d %H:%M:%S")


def greetings():
    return {
        "message": "What can I do for you?",
        "is_bot": True,
        "time": current_time()
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    contexts = [greetings()]
    history = json.dumps(contexts)
    return templates.TemplateResponse(
        "chats.html", {"request": request, "contexts": contexts, "history": history}
    )


@app.post("/", response_class=HTMLResponse)
def chats(
    request: Request,
    cmd: str = Form(...),
    message: str = Form(None),
    history: str = Form("[]"),
):
    if cmd == "clear":
        contexts = [greetings()]
    else:
        contexts = json.loads(history)
        if message:
            contexts.append({"message": message, "is_bot": False, "time": current_time()})
            chatgpt_raw_output = chat_completion(
                user_input=message,
                impersonated_role="",
                explicit_input="",
                chat_history="",
            )
            contexts.append({"message": chatgpt_raw_output, "is_bot": True, "time": current_time()})
    history = json.dumps(contexts)
    return templates.TemplateResponse(
        "chats.html",
        context={"request": request, "contexts": contexts, "history": history},
    )
