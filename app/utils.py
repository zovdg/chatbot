import pytz
import uuid
from datetime import datetime


def current_time() -> str:
    tz_sh = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz=tz_sh)
    return now.strftime("%Y/%m/%d %H:%M:%S")


def new_chat_id() -> str:
    return str(uuid.uuid4())
