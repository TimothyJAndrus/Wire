#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) <2019> <Jarad Dingman>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# STD LIB
import re

from sys import stdout
from inspect import stack

# EXTERNAL DEPS
from loguru import logger
from colorama import Fore, Style
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


@typechecked
def valid_url(url: str) -> bool:
    """
        Function to check that a url is valid

        @param url : str -> The url to test against the regex
    """
    return True if re.match(URL_REGEX, url) else False


def log(channel, mname, fname, message):
    channel(
        f"{Style.BRIGHT}{Fore.CYAN}{mname}{Style.RESET_ALL}:{Style.BRIGHT}{Fore.CYAN}{fname}{Style.RESET_ALL} 〉 {message}"
    )


def func_name() -> str:
    """ 
        Get the name of a function or method without messing with the 
        stack everywhere

        @returns str
    """
    return stack()[1][3]
