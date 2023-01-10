#
# This file is part of the Ingram Micro CloudBlue Connect Processors Toolkit.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from copy import deepcopy
from logging import Logger, LoggerAdapter
from typing import Any, Dict, List, Tuple, Union


class ExtensionLoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.get('extra', {})
        extra.update(self.extra)
        kwargs['extra'] = extra

        if 'request_id' in extra:
            msg = f"{extra.get('request_id')} {msg}"

        return msg, kwargs


def bind_logger(logger: Union[LoggerAdapter, Logger], request: dict) -> LoggerAdapter:
    """
    Binds the logger to the given request by attaching the id and some
    additional information to the extra data of the logger adapter.

    :param logger: LoggerAdapter The logger to bind with the request.
    :param request: Union[RequestBuilder, dict] The request to extract the ids.
    :return: LoggerAdapter
    """
    if not isinstance(request, dict):
        return logger

    from_request = {
        'request_id': request.get('id'),
        'request_type': request.get('type'),
        'request_status': request.get('status'),
    }

    if request_model(request) == 'asset':
        from_request['tier_id'] = request.get('asset', {}).get('tiers', {}).get('customer', {}).get('id')
        from_request['asset_id'] = request.get('asset', {}).get('id')

    elif request_model(request) == 'tier-config':
        from_request['tier_id'] = request.get('configuration', {}).get('account', {}).get('id')
        from_request['tier_config_id'] = request.get('configuration', {}).get('id')

    return ExtensionLoggerAdapter(
        logger.logger,
        {
            **logger.extra,
            **{k: v for k, v in from_request.items() if v is not None},
        },
    )


def mask_dictionary(data: Union[Dict, List, Tuple, Any], to_mask: List[str]) -> Union[Dict, List, Tuple, Any]:
    """
    Mask the required values by key in a dictionary.

    :param data: The dictionary to mask.
    :param to_mask: The list of keys to be masked.
    :return: The masked dictionary (it's a copy of the original).
    """
    if isinstance(data, dict):
        data = deepcopy(data)
        for key in data.keys():
            if key in to_mask:
                data[key] = '*' * len(str(data[key]))
            else:
                data[key] = mask_dictionary(data[key], to_mask)
        return data
    elif isinstance(data, (list, tuple)):
        return [mask_dictionary(item, to_mask) for item in data]
    else:
        return data


def request_model(request: dict) -> str:
    """
    Returns the request model depending on the request type.

    :param request: dict
    :return: str
    """

    def match_request_type(model: dict) -> bool:
        return model.get('object') in request or request.get('type') in model.get('types')

    try:
        return next(filter(match_request_type, [
            {
                'request': 'asset',
                'object': 'asset',
                'types': ['adjustment', 'purchase', 'change', 'suspend', 'resume', 'cancel'],
            },
            {
                'request': 'tier-config',
                'object': 'configuration',
                'types': ['setup'],
            },
        ])).get('request')
    except StopIteration:
        return 'undefined'
