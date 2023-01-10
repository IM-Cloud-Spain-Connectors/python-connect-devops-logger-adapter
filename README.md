# Python Connect DevOps Logger Adapter

[![Test](https://github.com/othercodes/python-connect-devops-logger-adapter/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-connect-devops-logger-adapter/actions/workflows/test.yml)

Extended Connect logger adapter that adds extra fields and prepend the request id to each message.

| Field          | Section | Description                                                                            |
|----------------|---------|----------------------------------------------------------------------------------------|
| message        | Message | The actual message text.                                                               |
| request_id     | Message | The id of the request that is being processed.                                         |
| request_type   | Extra   | Purchase, Cancel, Change, Suspend, Resume, Adjustment, Setup, Update.                  |
| request_status | Extra   | Pending, Tier-Setup, Draft, Approved, Inquiring, Failed, Scheduled, Revoking, Revoked. |
| account_id     | Extra   | Built-in. Optional. The Connect customer account id.                                   |
| account_name   | Extra   | Built-in. Optional. The Connect customer account name.                                 |
| tier_id        | Extra   | The Tier account id.                                                                   |
| tier_config_id | Extra   | Optional. The Connect tier config id.                                                  |
| asset_id       | Extra   | Optional. The Connect assert id.                                                       |

## Installation

The easiest way to install the Connect DevOps Logger Adapter is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-connect-devops-logger-adapter
# using pip
pip install rndi-connect-devops-logger-adapter
```

## The Contract

The used interface is the python build-in `logging.LoggerAdapter`.

## The Adapter

The usage of the adapter is quite easy, you just need to import it and call the `bind_logger` function using the logger
and the request you want to bind. A new instance of LoggerAdapter will be returned with all the required data attached.

```python
import logging
from rndi.connect_devops_logger_adapter.adapter import bind_logger

request = {
    'id': 'PR-1000-2000-3000-4000-001',
    'type': 'purchase',
    'status': 'pending'
    # ...
}

logger = bind_logger(logging.getLogger('MyLogger'), request)

logger.info('Hello world')  # output: PR-1000-2000-3000-4000-001 Hello world
```

Alternatively, you can use the `WithBoundedLogger` that exposes the `bind_logger` method, this way you can easily bind
the logger from your extension.

```python
from logging import LoggerAdapter
from rndi.connect_devops_logger_adapter.mixins import WithBoundedLogger


class SomeBusinessTransaction(WithBoundedLogger):
    def __init__(self, logger: LoggerAdapter):
        self.logger = logger

    def process(self, request: dict):
        self.logger.info('Hello world')  # output: Hello world

        # bind the logger to the request. 
        self.bind_logger(request)

        self.logger.info('Hello world')  # output: PR-1000-2000-3000-4000-001 Hello world
```
