from sys import stdout
from loguru import logger

config = {
    "handlers": [
        {
            "sink": stdout,
            "format": "\r<green>{time: MM/DD/YYYY HH:mm:ss}</green>"
            + " | <level>{level: <7}</level>"
            + " | <level>{message}</level>",
        }
    ]
}
logger.configure(**config)
