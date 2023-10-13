from logging import Logger, getLogger, NullHandler, DEBUG


def get_app_logger(name: str) -> Logger:
    logger = getLogger(name)
    logger.addHandler(NullHandler())
    logger.setLevel(DEBUG)
    logger.propagate = True
    return logger
