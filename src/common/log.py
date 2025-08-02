import logging
import sys

_formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
)

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(_formatter)


def get_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

    return logger
