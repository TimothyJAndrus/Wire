#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from wire.browser import *


@pytest.mark.incremental
class Test_Elements:

    def test_get_element_by_id(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            id = b.find_element_by_xpath("//div[@id]").get_attribute("id")
            assert b[f"#{id}"]

    def test_get_element_by_class(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            classx = b.find_element_by_xpath("//div[@class]").get_attribute("class")
            assert b[f".{classx}"]

    def test_get_element_by_xpath(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            assert b["*//div[@id]"]

    def test_get_element_by_tag(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            assert b["~div"]

    def test_get_element_by_css(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            assert b["_#viewport"]

    @pytest.mark.xfail(raises=ValueError)
    def test_get_element_invalid_identifier(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            assert b["o"]

    def test_get_element_missing(self):
        with Chrome(True) as b:
            b.get("https://google.com")
            assert b[".selenium_testing_is_rough_sometimes"] is None