from logging.config import dictConfig

from core.settings import get_settings

settings = get_settings()


def setup_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": ("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "handlers": ["console"],
            },
        }
    )
