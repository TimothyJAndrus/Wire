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

# STD LIB imports
import copy
import functools

from typing import Callable, List, Optional, Any
from types import TracebackType

# LOCAL DEPS
from wire.core.element import Element
from wire.utilities.helpers import valid_url, log, func_name
from wire.utilities.decorators import timer

# EXTERNAL DEPS
from loguru import logger
from typeguard import typechecked

# SELENIUM DEPS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Dictionary of identifiers to their respective locators
IDENTIFIERS = {
    "#": By.ID,
    "@": By.NAME,
    "*": By.XPATH,
    "~": By.TAG_NAME,
    ".": By.CLASS_NAME,
    "_": By.CSS_SELECTOR,
}

# TYPE ALIASES


class ToElementConverter(object):
    """
        Class used for decorating methods in the Browser class to 
        return a custom WebElement type
    """

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def __wrapper(driver: Browser, *args, **kwargs) -> List[Element]:
            result = func(driver, *args, **kwargs)
            if result is not None:
                return self.conversion(driver, result)
            return None

        return __wrapper

    @classmethod
    def conversion(
        cls, driver: Browser, elements: List[WebElement]
    ) -> List[Element]:
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


class Browser(webdriver.Firefox, webdriver.Chrome, webdriver.Remote):
    """
        This class overrides the firefox chrome and remote driver to
        allow true wrapping functionality. 
    """

    @typechecked
    def __init__(self, headless: bool = False, remote: str = "") -> None:
        """
            Browser class that acts as the parent wrapper
            to the selenium api. Able to wrap both chrome and firefox
            based on subclasses

            @param head: bool -> whether the browser will be
                                headless or not.
            @returns None
        """

        if self.classname not in ["Firefox", "Chrome"]:
            raise ValueError(f"Browser type: {self.classname} not supported")

        self.options = (
            Firefox_Options()
            if self.classname == "Firefox"
            else Chrome_Options()
        )

        if headless:  # pragma: no cover
            self.options.add_argument("--headless")
            log(logger.info, self.classname, func_name(), "headless mode")

        self.remote = True if remote else False

        if remote:  # pragma: no cover
            webdriver.Remote.__init__(
                self,
                desired_capabilities=getattr(
                    DesiredCapabilities, self.classname.upper()
                ),
                command_executor=remote,
            )
        else:
            getattr(webdriver, self.classname).__init__(
                self,
                options=self.options,
                desired_capabilities=getattr(
                    DesiredCapabilities, self.classname.upper()
                ),
            )
            self.set_page_load_timeout(15)
            self.implicitly_wait(5)

        log(logger.info, self.classname, func_name(), "Browser instantiated")

    def __enter__(self) -> Browser:
        """
            The enter dunder for contexts

            @returns Browser
        """
        return self

    def __exit__(
        self, typex: Any, value: Any, tb: Optional[TracebackType]
    ) -> None:
        """
            Exit dunder for the closing of both the object
            or a context surrounding the object

            @param type ->
            @param value ->
            @param traceback ->
            @returns None
        """
        if self.remote:  # pragma: no cover
            webdriver.remote.quit(self)
        else:
            getattr(webdriver, self.classname).quit(self)
        log(logger.info, self.classname, func_name(), "Destroyed browser")

    @typechecked
    def __str__(self) -> str:
        """
            Dunder for representing the object as a string

            @returns string
        """
        return self.classname

    @typechecked
    def __repr__(self) -> str:
        """
            Dunder for representing the object as a string

            @returns string
        """
        return self.__str__()

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
            return self.__wait_for(typex, elem, delay)
        except TimeoutException:
            return None

    @typechecked
    def __call__(self, url: str) -> bool:
        """
            Basically a wrapper around get for those who want to save
            the keystrokes

            @param url: str -> The url to visit
        """
        return self.get(url)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __wait_for(
        self, identifier: By, elem: str, delay: int
    ) -> List[Element]:
        """
            A method for explicit waits

            Shouldn't be called directly... necessarily

            @param identifier : By -> Locator
            @param element : str -> A webelement to find with an identifier
            @param delay : int -> Amount of time to wait in seconds
            @returns List of Elements
        """

        log(
            logger.info,
            self.classname,
            func_name(),
            f"Waiting on element: [{identifier}] -> {elem[1:]}",
        )

        WebDriverWait(self, delay).until(
            EC.presence_of_element_located((identifier, elem[1:]))
        )

        return self.find_elements(identifier, elem[1:])

    @timer
    @typechecked
    def get(self, url: str) -> bool:
        """
            Function to wrap seleniums get method

            @param url : str
        """
        if valid_url(url):
            log(logger.info, self.classname, func_name(), f"Retrieving: {url}")
            try:
                super(Browser, self).get(url)
            except TimeoutException:  # pragma: no cover
                log(
                    logger.warning,
                    self.classname,
                    func_name(),
                    f"{url} raised a timeout exception",
                )
                return False
            return True

        log(
            logger.warning,
            self.classname,
            func_name(),
            f"{url} is not a valid url",
        )
        return False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @property
    def classname(self):
        """
            Function to get the name of the class without
            using the ugly dunder method

            @returns string
        """
        return self.__class__.__name__

    @property
    def links(self) -> Optional[List[str]]:
        """
            Function to get a list of where all links on a page point to
        """
        return [
            x.get_attribute("href")
            for x in self.find_elements_by_xpath("//a[@href]")
        ]

    @property
    def url(self) -> str:
        """
            Access the url as if it was a member variable
        """
        return self.current_url

    @property
    def source(self) -> str:
        """
            Access the page source as if it was a member variable
        """
        return self.page_source


# Alias
class Firefox(Browser):
    pass


# Alias
class Chrome(Browser):
    pass
