#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from wire.element import ToElementConverter
from wire.helpers import identifiers

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def wait_on_item(driver, elem: str):
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
        typex = identifiers.identifier_table[elem[0]]
        return wait_for(driver, typex, elem)
    except KeyError:
        raise ValueError("Missing valid identifier")
    except TimeoutException:
        return None


def wait_for(driver, identifier, elem):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((identifier, elem[1:]))
    )
    return driver.find_elements(identifier, elem[1:])
