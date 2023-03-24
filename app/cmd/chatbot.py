import sys

sys.path.extend(["./"])

import uvicorn
from app.config import settings

from app.logger import init_logger
from app.application import app


if __name__ == "__main__":
    init_logger(debug=settings.debug)

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="debug" if settings.debug else "info",
    )
