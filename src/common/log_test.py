import logging

from . import log


def test_get_logger_root() -> None:
    logger = log.get_logger()

    assert logger.name == 'root'
    assert logger.level == logging.INFO


def test_get_logger_new() -> None:
    logger = log.get_logger('test')

    assert logger.name == 'test'
    assert logger.level == logging.INFO
