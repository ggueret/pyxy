import os

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "loggers": {
        "pyxy": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True
        }
# Uncomment these lines to debug http requests
#        "urllib3": {
#            "handlers": ["default"],
#            "level": "DEBUG",
#            "propagate": True
#        }
    }
}

CACHE_DIR = os.getenv("PYXY_CACHE_DIR")
