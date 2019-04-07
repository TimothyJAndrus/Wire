#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

# standard libs
import copy
import functools

from typing import Callable

# LOCAL DEPS
from wire.helpers import identifiers
from wire.helpers import getelement

# ---------- External dependencies -------------- #
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.common.exceptions import TimeoutException, WebDriverException


class ToElementConverter(object):
    """
        Class used for decorating methods in the Browser class to 
        return a custom WebElement type
    """

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def __wrapper(driver, *args, **kwargs):
            result = func(driver, *args, **kwargs)
            if result is not None:
                return self.conversion(driver, result)
            return None

        return __wrapper

    @classmethod
    def conversion(cls, driver, elements):
        for index, element in enumerate(elements):
            elements[index] = cls.convert(element)
        return elements

    @classmethod
    def convert(cls, webelement: WebElement) -> Element:
        if isinstance(webelement, WebElement):
            element_class = copy.deepcopy(Element)
            element_class.__bases__ = tuple(
                FirefoxWebElement if base is WebElement else base
                for base in Element.__bases__
            )
        return Element(webelement)


class Element(WebElement):
    def __new__(cls, webelement: WebElement):
        instance = super(Element, cls).__new__(cls)
        instance.__dict__.update(webelement.__dict__)
        return instance

    # This method is REQUIRED to override the WebElement init method
    # Removing this will cause strange errors to we leave it :)
    def __init__(self, webelement: WebElement):
        pass

    def __getitem__(self, elem: str):
        return getelement.wait_on_item(self.parent, elem)

    @property
    def children(self):
        return self.__getitem__("*./*")
