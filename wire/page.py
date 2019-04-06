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


class PageMeta(type):
    def __new__(cls, name, bases, namespace):
        if "url" not in namespace:  # pragma: no cover
            raise ValueError("Class is missing its url param")
        return super().__new__(cls, name, bases, namespace)


class Page(object, metaclass=PageMeta):

    url = ""
    elements = {}

    def __init__(self, driver) -> None:
        """
            The initializer for the Page objects

            @param driver : Browser -> the driver object to use
        """
        self._driver = driver
        self._driver.get(self.url)

        for key, value in self.elements.items():
            if isinstance(value, list):
                index = 0 if len(value) > 1 else value[1]
                value = value[0]
            else:
                index = 0
                value = value

            elements = self.__getitem__(value)
            if elements:
                setattr(self, key, elements[index])
            else:
                pass  # What to do if none is returned

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.url})"

    def __getitem__(self, identifier: str):
        return self._driver[identifier]
