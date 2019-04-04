#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from wire.browser import *


@pytest.mark.incremental
class Test_Chrome_Browser_Getter:
    def test_google(self):
        with Chrome(True) as b:
            assert b.get("http://google.com")

    def test_malformed_url(self):
        with Chrome(True) as b:
            assert b.get("") == False

    def test_malformed_url_2(self):
        with Chrome(True) as b:
            assert b.get("af/.amsf,/.,/a") == False

    @pytest.mark.xfail(raises=TypeError)
    def test_malformed_url_3(self):
        with Chrome(True) as b:
            b.get(0)

    @pytest.mark.xfail(raises=TypeError)
    def test_malformed_url_4(self):
        with Chrome(True) as b:
            b.get([])


@pytest.mark.incremental
class Test_Firefox_Browser_Getter:
    def test_google(self):
        with Firefox(True) as b:
            assert b.get("http://google.com")

    def test_malformed_url(self):
        with Firefox(True) as b:
            assert b.get("") == False

    def test_malformed_url_2(self):
        with Firefox(True) as b:
            assert b.get("af/.amsf,/.,/a") == False

    @pytest.mark.xfail(raises=TypeError)
    def test_malformed_url_3(self):
        with Firefox(True) as b:
            b.get(0)

    @pytest.mark.xfail(raises=TypeError)
    def test_malformed_url_4(self):
        with Firefox(True) as b:
            b.get([])
