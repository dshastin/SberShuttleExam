import logging
from logging import config as logging_config

from core.config import settings

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": settings.handlers_logging_lvl,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": settings.handlers_logging_lvl,
        },
        "uvicorn.error": {
            "level": settings.logger_logging_lvl,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": settings.logger_logging_lvl,
            "propagate": False,
        },
    },
    "root": {
        "level": settings.root_logging_lvl,
        "formatter": "verbose",
        "handlers": ["console"],
    },
}

logging_config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
