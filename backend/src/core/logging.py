import structlog
import logging
import sys
from contextvars import ContextVar
from typing import Optional

correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    def add_correlation_id(logger, method_name, event_dict):
        req_id = correlation_id.get()
        if req_id:
            event_dict["correlation_id"] = req_id
        return event_dict

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            add_correlation_id,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    return structlog.get_logger(name)
