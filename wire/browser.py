#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import functools

# External deps
from wire.helpers import identifiers
from wire.helpers import getelement
from wire.helpers import logging
from wire.helpers import timer
from wire.helpers import url

from wire.exceptions import InvalidBrowserException
from wire.element import ToElementConverter

# Selenium libs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.common.desired_capabilities import (
    DesiredCapabilities as DC,
)
from selenium.common.exceptions import TimeoutException, WebDriverException


class Browser(webdriver.Firefox, webdriver.Chrome, webdriver.Remote):
    def __init__(self, headless: bool = False, remote: str = ""):

        if self.__class__.__name__ not in ["Firefox", "Chrome"]:
            logging.logger.error(
                f"{self.__class__.__name__} is a bad browser type"
            )
            raise InvalidBrowserException(
                f"{self.__class__.__name__} is a bad browser type"
            )

        self.options = (
            FOptions() if self.__class__.__name__ == "Firefox" else COptions()
        )

        if headless:  # pragma: no cover
            self.options.add_argument("--headless")

        getattr(
            webdriver, ("Remote" if remote else self.__class__.__name__)
        ).__init__(
            self,
            options=self.options,
            desired_capabilities=getattr(DC, self.__class__.__name__.upper()),
            **({"command_executor": remote} if remote else {}),
        )

        logging.logger.info(f"Instance of {self.__class__.__name__} created")

        if headless:
            logging.logger.info(f"    -> Created in headless mode")

        self.set_page_load_timeout(15)
        self.implicitly_wait(5)

    def __enter__(self) -> Browser:
        return self

    def __exit__(self, typex, value, tb):
        getattr(
            webdriver, "Remote" if self._is_remote else self.__class__.__name__
        ).quit(self)
        logging.logger.info(f"Instance of {self.__class__.__name__} destroyed")

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return self.__str__()

    @ToElementConverter()
    def __getitem__(self, elem: str):
        return getelement.wait_on_item(self, elem)

    def __call__(self, url: str) -> bool:
        return self.get(url)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @timer.timer
    def get(self, vurl: str) -> bool:
        url.validate_url(vurl)

        try:
            super(Browser, self).get(vurl)
            logging.logger.info(f"Visit: {self.url}")
        except TimeoutException:  # pragma: no cover
            logging.logger.warning(f"{vurl} not retrieved before timeout")
            return False

        return True

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
