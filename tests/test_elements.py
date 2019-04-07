#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest

import wire


def test_element(wiretap):
    wiretap.get("https://google.com")
    elem = wiretap["*//div"][0]
    # print(elem, elem.children)
