#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import functools

from typing import Callable


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def __wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        return result

    return __wrapped
