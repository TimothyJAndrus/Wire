#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from functools import wraps
from inspect import getcomments

from wire.utilities.colors import *
from wire.utilities.utilities import log

# ---------- External dependencies -------------- #
from loguru import logger


# def logdoc(func):
#     """"""

#     @wraps(func)
#     def wrapped(*args, **kwargs):
#         fname = func.__qualname__.split(".")
#         if len(fname) == 2:
#             log(
#                 logger.info,
#                 fname[0],
#                 fname[1],
#                 getcomments(func).strip().replace("#", ""),
#             )

#         else:
#             mname = func.__globals__["__file__"].split(".")
#             log(
#                 logger.info,
#                 mname[0],
#                 fname[0],
#                 getcomments(func).strip().replace("#", ""),
#             )
#         return func(*args, **kwargs)

#     return wrapped


# def undocumented(func):
#     """This is a decorator which can be used to mark functions
#     as undocumented. It will result in a warning being emitted
#     when the function is used."""

#     @wraps(func)
#     def wrapped(*args, **kwargs):
#         fname = func.__qualname__.split(".")
#         if len(fname) == 2:
#             log(logger.warning, fname[0], fname[1], f"{Bo}{Y}Undocumented{E}")
#         else:
#             mname = func.__globals__["__file__"].split(".")
#             log(logger.warning, mname[0], fname[0], f"{Bo}{Y}Undocumented{E}")
#         return func(*args, **kwargs)

#     return wrapped


def timer(func):
    """This is a decorator which can be used to mark functions
    with a timer. It will result in a timer being started when the
    function is called and will output the time taken at the return
    of the function."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        start = time.time_ns()
        result = func(*args, **kwargs)
        logger.info("Page Load: " + str((time.time_ns() - start)))
        return result

    return wrapped


# class assert_raises(object):
#     # based on pytest and unittest.TestCase
#     def __init__(self, type):
#         self.type = type

#     def __enter__(self):
#         pass

#     def __exit__(self, type, value, traceback):
#         if type is None:
#             raise AssertionError("exception expected")
#         if issubclass(type, self.type):
#             return True  # swallow the expected exception
#         raise AssertionError("wrong exception type")


# with assert_raises(KeyError):
#     {}['foo']

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
