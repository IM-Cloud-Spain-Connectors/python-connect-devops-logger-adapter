from logging import LoggerAdapter
from unittest.mock import Mock

from rndi.connect.devops_logger_adapter.adapter import ExtensionLoggerAdapter, mask_dictionary
from rndi.connect.devops_logger_adapter.mixins import WithBoundedLogger


class Helper(WithBoundedLogger):
    def __init__(self, logger: LoggerAdapter):
        self.logger = logger


def test_bounded_logger_should_configure_logger_from_request_dictionary_asset():
    helper = Helper(LoggerAdapter(Mock(), {}))
    helper.bind_logger({
        'id': 'PR-123-456-789',
        'type': 'purchase',
        'status': 'pending',
    })

    assert helper.logger.extra.get('request_id') == 'PR-123-456-789'


def test_bounded_logger_should_configure_logger_from_request_dictionary_tier_config():
    helper = Helper(LoggerAdapter(Mock(), {}))
    helper.bind_logger({
        'id': 'TC-123-456-789',
        'type': 'setup',
        'status': 'pending',
    })

    assert helper.logger.extra.get('request_id') == 'TC-123-456-789'


def test_bounded_logger_should_not_configure_logger_from_invalid_request_dictionary():
    helper = Helper(LoggerAdapter(Mock(), {}))
    helper.bind_logger({})

    assert 'id' not in helper.logger.extra


def test_bounded_logger_should_not_configure_logger_from_not_a_request_dictionary():
    helper = Helper(LoggerAdapter(Mock(), {}))
    helper.bind_logger('Some invalid request')

    assert 'id' not in helper.logger.extra


def test_logger_should_attach_id_to_message_if_configured(make_logger):
    message = 'This is a cool log message'

    logger = ExtensionLoggerAdapter(
        make_logger(lambda level, msg, *arg, **kwargs: msg == f'SOME-ID {message}'),
        {'request_id': 'SOME-ID'},
    )

    logger.info(message)


def test_logger_should_not_attach_id_to_message_if_not_configured(make_logger):
    message = 'Hello world from the logger'

    logger = ExtensionLoggerAdapter(
        make_logger(lambda level, msg, *arg, **kwargs: msg == message),
        {},
    )

    logger.info(message)


def test_mask_function_should_mask_the_required_values():
    payload = {
        'id': '123456',
        'payload': {
            'key': 'mask-this-value',
            'users': [
                {'id': 1, 'password': '1'},
                {'id': 2, 'password': '22'},
                {'id': 3, 'password': '333'},
            ],
        },
    }

    expected = {
        'id': '123456',
        'payload': {
            'key': '***************',
            'users': [
                {'id': 1, 'password': '*'},
                {'id': 2, 'password': '**'},
                {'id': 3, 'password': '***'},
            ],
        },
    }

    assert mask_dictionary(payload, ['key', 'password']) == expected
