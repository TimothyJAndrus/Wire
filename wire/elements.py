#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from types import TracebackType
from typing import Optional, Any, Union, List, Dict

# ---------- External dependencies -------------- #
from loguru import logger
from typeguard import typechecked

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Element(WebElement):

    def __new__(cls, webelement):
        instance = super(Element, cls).__new__(cls)
        instance.__dict__.update(webelement.__dict__)
        return instance

    # def __init__(self, webelement):
    #     pass

    @property
    def test(self):
        return("pewpew")