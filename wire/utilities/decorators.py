#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import functools

from typing import Callable

# LOCAL DEPS

# ---------- External dependencies -------------- #
from loguru import logger
from typeguard import typechecked


def timer(func: Callable) -> Callable:
    """
        This is a decorator which can be used to mark functions
        with a timer. It will result in a timer being started when the
        function is called and will output the time taken at the return
        of the function.

        @param func : Callable -> Funciton to wrap
        @returns Callable    
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        # FIX ME :)
        logger.info("Page Load: " + str((time.time() - start)))
        return result

    return wrapped


# def undocumented(func: Callable) -> Callable:
#     """
#         This is a decorator which can be used to mark functions
#         as undocumented. It will result in a warning being emitted
#         when the function is used.

#         @param func : Callable -> Function to wrap
#         @returns Callable
#     """

#     @functools.wraps(func)
#     def __wrapped(*args, **kwargs):
#         fname = func.__qualname__.split(".")
#         if len(fname) == 2:
#             log(logger.warning, fname[0], fname[1], f"{Bo}{Y}Undocumented{E}")
#         else:
#             mname = func.__globals__["__file__"].split(".")
#             log(logger.warning, mname[0], fname[0], f"{Bo}{Y}Undocumented{E}")
#         return func(*args, **kwargs)

#     return __wrapped

# class WordProcessor(object):
#     PLUGINS = []
#     def process(self, text):
#         for plugin in self.PLUGINS:
#             text = plugin().cleanup(text)
#         return text

#     @classmethod
#     def plugin(cls, plugin):
#         cls.PLUGINS.append(plugin)

# @WordProcessor.plugin
# class CleanMdashesExtension(object):
#     def cleanup(self, text):
#         return text.replace('&mdash;', u'\N{em dash}')
