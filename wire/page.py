#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from wire.helpers import getelement

from wire.element import ToElementConverter


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

    @ToElementConverter()
    def __getitem__(self, identifier: str):
        return getelement.wait_on_item(self._driver, identifier)
