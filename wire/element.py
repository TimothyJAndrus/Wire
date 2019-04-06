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

from __future__ import annotations

# standard libs
import copy
import functools

from typing import List, Callable, Optional

from loguru import logger
from typeguard import typechecked

# LOCAL DEPS
from wire.utilities.constants import IDENTIFIERS
from wire.utilities.helpers import log, func_name

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
        def __wrapper(driver, *args, **kwargs) -> List[Element]:
            result = func(driver, *args, **kwargs)
            if result is not None:
                return self.conversion(driver, result)
            return None

        return __wrapper

    @classmethod
    def conversion(cls, driver, elements: List[WebElement]) -> List[Element]:
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

    @typechecked
    @ToElementConverter()
    def __getitem__(
        self, elem: str, delay: int = 5
    ) -> Optional[List[Element]]:
        """ 
            JQuery-esque element finding function

            Keyword arguments:
            element -- the element to find given an identifier
                .   -- class
                #   -- id
                _   -- css
                *   -- xpath
                @   -- name
                ~   -- tag name

            @param elem: str -> The string to identify the element
            @param delay: int -> The time to wait for the element to show
            @returns List of Elements
        """
        try:
            typex = IDENTIFIERS[elem[0]]
        except KeyError:
            raise ValueError("Missing valid identifier")

        try:
            log(
                logger.info,
                self.classname,
                func_name(),
                f"Waiting on element: [{typex}] -> {elem[1:]}",
            )

            WebDriverWait(self, delay).until(
                EC.presence_of_element_located((typex, elem[1:]))
            )

            return self.find_elements(typex, elem[1:])
        except TimeoutException:
            return None

    @property
    def children(self) -> Optional[List[Element]]:
        return self.__getitem__("*./*")

    @property
    def classname(self):
        return self.__class__.__name__
