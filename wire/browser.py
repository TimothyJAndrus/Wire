#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from types import TracebackType
from typing import Optional, Any, Union, List, Dict

# --------- Local dependencies ------------------ #
from wire.utilities.colors import *
from wire.utilities.utilities import *
from wire.utilities.decorators import *

# ---------- External dependencies -------------- #
from loguru import logger
from typeguard import typechecked

# ////////// Selenium imports //////////// #
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# TODO:
"""
    assert catching decorator
    __enter__ exception handler for strings and crap
    Plugins
    split library into more files :)
"""

BY_TYPES = {
    ".": By.CLASS_NAME,
    "#": By.ID,
    "_": By.CSS_SELECTOR,
    "*": By.XPATH,
    "@": By.NAME,
    "~": By.TAG_NAME,
}

class Browser(webdriver.Firefox, webdriver.Chrome, webdriver.Remote):
    @typechecked
    def __init__(self, head: bool = False, remote: str = "") -> None:
        """
            Browser class that acts as the parent wrapper
            to the selenium api. Able to wrap both chrome and firefox
            based on subclasses

            @param head: bool -> whether the browser will be
                                headless or not.
            @returns None
        """
        if self.sn not in ["Firefox", "Chrome"]:
            raise ValueError(f"Browser type not supported yet", type(self))

        self.options = (
            Firefox_Options() if self.sn == "Firefox" else Chrome_Options()
        )

        if head:  # pragma: no cover
            self.options.add_argument("--headless")
            log(logger.info, self.sn, xfunc(), "headless mode")

        if remote:
            self.remote = True
            webdriver.Remote.__init__(
                self,
                desired_capabilities=getattr(
                    DesiredCapabilities, self.sn.upper()
                ),
                command_executor=remote,
            )
        else:
            getattr(webdriver, self.sn).__init__(
                self,
                options=self.options,
                desired_capabilities=getattr(
                    DesiredCapabilities, self.sn.upper()
                ),
            )
            self.set_page_load_timeout(5)
            self.implicitly_wait(5)

        log(logger.info, self.sn, xfunc(), "Browser instantiated")

    def __enter__(self) -> Browser:
        """
            The enter dunder for contexts

            @returns Browser
        """
        return self

    def __exit__(
        self, type: Any, value: Any, traceback: Optional[TracebackType]
    ) -> None:
        """
            Exit dunder for the closing of both the object
            or a context surrounding the object

            @param type ->
            @param value ->
            @ param traceback ->
            @returns None
        """
        if self.remote:
            webdriver.remote.quit(self)
        else:
            getattr(webdriver, self.sn).quit(self)
        log(logger.info, self.sn, xfunc(), "Destroyed browser")

    def __str__(self) -> str:
        """
            Dunder for representing the object as a string

            @returns string
        """
        return self.sn

    def __repr__(self) -> str:
        """
            Dunder for representing the object as a string

            @returns string
        """
        return self.__str__()

    @typechecked
    def __getitem__(
        self, elem: str, delay: int = 5
    ) -> Optional[Union[List, WebElement]]:
        """ JQuery-esque element finding function

        Keyword arguments:
        element -- the element to find given an identifier
            .   -- class
            #   -- id
            _   -- css
            *   -- xpath
            @   -- name
            ~   -- tag name
        """
        try:
            type = BY_TYPES[elem[0]]
        except KeyError:
            raise ValueError("Missing valid identifier")

        try:
            return self.__wait_for(type, elem, delay)
        except TimeoutException:
            return None

    ###########################################################
    ### END DUNDER ############################################
    ###########################################################

    # def __wait_on(self, *args):
    #     # Function for waiting on 1 of many conditions
    #     pass

    def __wait_for(self, type: By, elem: str, delay: int) -> List[Webelement]:
        """
            A method for explicit waits

            Shouldn't be called directly... necessarily

            Keyword arguments:
            element -- A webelement to find with an identifier
            delay   -- Amount of time to wait in seconds
        """

        log(
            logger.info,
            self.sn,
            xfunc(),
            f"Waiting on element: [{type}] -> {elem[1:]}",
        )

        WebDriverWait(self, delay).until(
            EC.presence_of_element_located((type, elem[1:]))
        )

        return self.find_elements(type, elem[1:])

    @timer
    @typechecked
    def get(self, url: str) -> bool:
        """
            Function to wrap seleniums get method

            @param url : str
        """
        if valid_url(url):
            log(logger.info, self.sn, xfunc(), f"Retrieving: {url}")
            super(Browser, self).get(url)
            return True

        log(logger.warning, self.sn, xfunc(), f"{url} is not a valid url")
        return False

    #########################################################
    #### Props  #############################################
    #########################################################

    @property
    def sn(self) -> str:
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
