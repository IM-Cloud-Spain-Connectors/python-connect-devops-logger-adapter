from logging import LoggerAdapter
from typing import Callable
from unittest.mock import patch

import pytest


@pytest.fixture
def make_logger():
    def __(log: Callable[[int, str, list, dict], None] = lambda _: None) -> LoggerAdapter:
        with patch('logging.LoggerAdapter') as logger:
            logger.log = log

        return logger

    return __
