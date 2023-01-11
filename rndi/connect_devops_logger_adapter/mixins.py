#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from logging import LoggerAdapter

from rndi.connect_devops_logger_adapter.adapter import bind_logger


class WithBoundedLogger:
    logger: LoggerAdapter

    def bind_logger(self, request: dict) -> LoggerAdapter:
        self.logger = bind_logger(self.logger, request)
        return self.logger
