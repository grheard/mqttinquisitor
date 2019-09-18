import logging
import logging.config


# Define the logging configuration
LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": "False",
    "root": {
        "level": "DEBUG",
        "handlers": ["console"]
    },
    "formatters": {
        "long": {
            "format": "%(asctime)s  %(levelname)-8s  %(filename)-20s  %(funcName)-20s  %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "long"
        }
    }
}


def custom_logger():
    _logger = logging.getLogger()

    if not _logger.hasHandlers():
        logging.config.dictConfig(LOGGING_CFG)

    return _logger


logger = custom_logger()
