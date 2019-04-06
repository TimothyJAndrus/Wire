#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest

import wire


class LoginPage(wire.Page):

    url = "https://google.com"


def test_page(wiretap):
    LoginPage(wiretap)


def test_page_str(wiretap):
    login_page = LoginPage(wiretap)
    assert str(login_page) == "LoginPage(https://google.com)"
