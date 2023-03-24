import logging


def init_logger(debug=False, filename=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    ch = logging.StreamHandler()
    # fh = logging.FileHandler(filename=filename)
    # fh = logging.handlers.RotatingFileHandler(filename, mode="a", maxBytes=100*1024, backupCount=3)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(module)s.%(funcName)s:%(lineno)d %(message)s"
    )

    ch.setFormatter(formatter)
    # fh.setFormatter(formatter)

    logger.addHandler(ch)
    # logger.addHandler(fh)
