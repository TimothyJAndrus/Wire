#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from sys import stdout
from inspect import stack

# Local dependencies
from wire.utilities.colors import E, Bo, B, Y

# External dependencies
from loguru import logger

from typeguard import typechecked

# -----------------------------------------------+---+---+
#      Dont mind me here                         | _ | X |
# -----------------------------------------------+---+---+
config = {
    "handlers": [
        {
            "sink": stdout,
            "format": "\r<green>{time: MM/DD/YYYY HH:mm:ss.SSS}</green>"
            + " | <level>{level: <8}</level>"
            + " | <level>{message}</level>",
        }
    ]
}
logger.configure(**config)
# -------------------------------------------------------+

URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def log(channel, mname, fname, message):
    channel(f"{Bo}{B}{mname}{E}:{Bo}{B}{fname}{E} 〉 {message}")


@typechecked
def valid_url(url: str) -> bool:
    return True if re.match(URL_REGEX, url) else False


def xfunc() -> str:
    """ This allows subclasses to get the name of
        the function without doing weird stack magic. :)"""
    return stack()[1][3]
