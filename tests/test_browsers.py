#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest

from wire.browser import Chrome, Firefox, Browser


class Test_Bad_Browser:
    @pytest.mark.xfail(raises=ValueError)
    def test_bad(self):
        b = Browser(True)


@pytest.mark.smoke
@pytest.mark.incremental
@pytest.mark.usefixtures("wiretap")
class TestDunders:
    def test_init(self):

        newBrowser = Firefox(True)
        del newBrowser

        newBrowser = Chrome(True)
        del newBrowser

    def test_call(self):
        self.wire("https://google.com")
        assert self.wire.url == "https://www.google.com/"

    def test_str(self):
        assert str(self.wire) in ["Firefox", "Chrome"]

    def test_repr(self):
        assert repr(self.wire) in ["Firefox", "Chrome"]

    def test_context(self):
        with Chrome(True) as _:
            assert True

        with Firefox(True) as _:
            assert True

    def test_getitem_class(self):
        self.wire.get("https://google.com")
        classx = self.wire["*//a[@class]"][0].get_attribute("class")
        assert self.wire[f".{classx}"]

    def test_getitem_id(self):
        self.wire.get("https://google.com")
        xid = self.wire["*//a[@id]"][0].get_attribute("id")
        assert self.wire[f"#{xid}"]

    def test_getitem_name(self):
        self.wire.get("https://google.com")
        name = self.wire["*//input[@name]"][0].get_attribute("name")
        assert self.wire[f"@{name}"]

    def test_getitem_tag(self):
        self.wire.get("https://google.com")
        assert self.wire["~div"]

    def test_getitem_xpath(self):
        self.wire.get("https://google.com")
        assert self.wire[f"*//input[@name]"]

    def test_getitem_css(self):
        self.wire.get("https://google.com")
        assert self.wire[f"_#viewport"]

    @pytest.mark.xfail(raises=ValueError)
    def test_getitem_missing_identifier(self):
        self.wire.get("https://google.com")
        assert self.wire["o"]

    def test_getitem_empty(self):
        self.wire.get("https://google.com")
        assert self.wire[""] is None

    @pytest.mark.xfail(raises=TypeError)
    def test_getitem_bad_type(self):
        self.wire.get("https://google.com")
        assert self.wire[1] is None

    def test_getitem_nonexistent(self):
        assert self.wire[".lkjsdlfjklsajfd"] is None

    def test_get(self):
        self.wire.get("https://google.com")
        assert self.wire.url == "https://www.google.com/"

    @pytest.mark.xfail(raises=AssertionError)
    def test_bad_get(self):
        assert self.wire.get("lasjfkjoiewjfnjonodsangl")

    def test_links(self):
        assert self.wire.links

    def test_source(self):
        assert self.wire.source

    def test_display_source(self):
        self.wire.get("https://google.com")
        self.wire.print_source()
