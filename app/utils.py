import pytz

from datetime import datetime


def current_time():
    tz_sh = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz=tz_sh)
    return now.strftime("%Y/%m/%d %H:%M:%S")
