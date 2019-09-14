import logging
import logging.config


# Define the logging configuration
LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": "False",
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },
    "formatters": {
        "long": {
            "format": "%(asctime)s  %(levelname)-8s  %(filename)-20s  %(funcName)-10s  %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "long"
        }
    },
    "loggers": {
        "debug": {
            "handlers": ["console"],
            "level": "DEBUG"
        },
        "verbose": {
            "handlers": ["console"],
            "level": "INFO"
        },
    }
}


def custom_logger(env_key='LOG_CFG'):
    _logger = logging.getLogger()

    # Load the configuration
    logging.config.dictConfig(LOGGING_CFG)

    return _logger


logger = custom_logger()
