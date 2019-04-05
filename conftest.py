import os
import sys
import pytest

import importlib

# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from wire.browser import Chrome, Firefox, Browser


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run headless browser",
    )


def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browsers = ["Firefox", "Chrome"]
        metafunc.parametrize("browser", browsers, scope="session")


@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless")


@pytest.fixture(scope="class")
def wiretap(request, browser, headless):
    with globals()[browser](head=headless) as Wire:
        if request.cls is not None:
            request.cls.wire = Wire
        yield Wire


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)
