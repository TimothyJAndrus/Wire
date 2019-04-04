#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from wire.browser import *


class Test_Bad_Browser:

    @pytest.mark.xfail(raises=ValueError)
    def test_chrome_without_head_value(self):
        with Browser(False) as _:
            pass

@pytest.mark.incremental
class Test_Chrome_Browser_Instantiation:
    def test_chrome_without_head_value(self):
        with Chrome(False) as _:
            pass

    def test_name(self):
        with Chrome(False) as _:
            assert str(_) == "Chrome"

    def test_links(self):
        with Chrome(True) as _:
            _.get("https://google.com")
            assert repr(_) == str(_)

    def test_url(self):
        with Chrome(True) as _:
            _.get("https://google.com")
            assert _.url == "https://www.google.com/"

    # find a better way to test the source code
    def test_source(self):
        with Chrome(True) as _:
            _.get("https://google.com")
            assert True

    def test_links(self):
        with Chrome(True) as _:
            _.get("https://google.com")
            assert len(_.links) > 1

    @pytest.mark.parametrize("head", [(1), ("1"), ([]), ({})])
    @pytest.mark.xfail(raises=TypeError)
    def test_chrome_with_head_bad_value(self, head):
        with Chrome(head) as _:
            pass

    @pytest.mark.parametrize("head", [(True), (False)])
    def test_chrome_with_head_value(self, head):
        with Chrome(head) as _:
            pass

    @pytest.mark.xfail(raises=TypeError)
    def test_chrome_bad_value(self):
        with Chrome("False") as _:
            pass


@pytest.mark.incremental
class Test_Firefox_Browser_Instantiation:
    def test_firefox_without_head_value(self):
        with Firefox(False) as _:
            pass

    def test_name(self):
        with Firefox(True) as _:
            assert str(_) == "Firefox"

    @pytest.mark.parametrize("head", [(1), ("1"), ([]), ({})])
    @pytest.mark.xfail(raises=TypeError)
    def test_firefox_with_head_bad_value(self, head):
        with Firefox(head) as _:
            pass

    @pytest.mark.parametrize("head", [(True), (False)])
    def test_firefox_with_head_value(self, head):
        with Firefox(head) as _:
            pass

    @pytest.mark.xfail(raises=TypeError)
    def test_firefox_bad_value(self):
        with Firefox("False") as _:
            pass
