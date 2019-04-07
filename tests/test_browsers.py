#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest

import wire
from wire.browser import Browser
from wire.exceptions import *


def test_init():
    newBrowser = wire.Firefox(True)
    del newBrowser

    newBrowser = wire.Chrome(True)
    del newBrowser


def test_call(wiretap):
    wiretap("https://google.com")
    assert wiretap.url == "https://www.google.com/"


def test_str(wiretap):
    assert str(wiretap) in ["Firefox", "Chrome"]


def test_repr(wiretap):
    assert repr(wiretap) in ["Firefox", "Chrome"]


def test_context(wiretap):
    with wire.Chrome(True) as _:
        assert True
    with wire.Firefox(True) as _:
        assert True


def test_getitem_class(wiretap):
    wiretap.get("https://google.com")
    classx = wiretap["*//a[@class]"][0].get_attribute("class")
    assert wiretap[f".{classx}"]


def test_getitem_id(wiretap):
    wiretap.get("https://google.com")
    xid = wiretap["*//a[@id]"][0].get_attribute("id")
    assert wiretap[f"#{xid}"]


def test_getitem_name(wiretap):
    wiretap.get("https://google.com")
    name = wiretap["*//input[@name]"][0].get_attribute("name")
    assert wiretap[f"@{name}"]


def test_getitem_tag(wiretap):
    wiretap.get("https://google.com")
    assert wiretap["~div"]


def test_getitem_xpath(wiretap):
    wiretap.get("https://google.com")
    assert wiretap[f"*//input[@name]"]


def test_getitem_css(wiretap):
    wiretap.get("https://google.com")
    assert wiretap[f"_#viewport"]


def test_getitem_missing_identifier(wiretap):
    wiretap.get("https://google.com")
    with pytest.raises(ValueError):
        assert wiretap["o"]


def test_getitem_empty(wiretap):
    wiretap.get("https://google.com")
    with pytest.raises(IndexError):
        assert wiretap[""] is None


def test_getitem_bad_type(wiretap):
    wiretap.get("https://google.com")
    with pytest.raises(TypeError):
        assert wiretap[1] is None


def test_getitem_nonexistent(wiretap):
    assert wiretap[".lkjsdlfjklsajfd"] is None


def test_get(wiretap):
    wiretap.get("https://google.com")
    assert wiretap.url == "https://www.google.com/"


def test_bad_get(wiretap):
    with pytest.raises(InvalidURLException):
        assert wiretap.get("lasjfkjoiewjfnjonodsangl") is None


def test_links(wiretap):
    wiretap.get("https://google.com")
    assert wiretap.links


def test_source(wiretap):
    wiretap.get("https://google.com")
    assert wiretap.source


def test_bad():
    with pytest.raises(InvalidBrowserException):
        b = Browser(True)
        b.reload()


# @pytest.mark.smoke
# @pytest.mark.incremental
