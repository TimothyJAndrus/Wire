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

# ---------- External dependencies -------------- #
from loguru import logger
from typeguard import typechecked

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.common.exceptions import TimeoutException, WebDriverException


class Element(WebElement):
    def __new__(cls, webelement: WebElement):
        instance = super(Element, cls).__new__(cls)
        instance.__dict__.update(webelement.__dict__)
        return instance

    # This method is REQUIRED to override the WebElement init method
    # Removing this will cause strange errors to we leave it :)
    def __init__(self, webelement: WebElement):
        pass

    @property
    def test(self):
        return "pewpew"
