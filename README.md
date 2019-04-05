
<h1 align="center">
    Wire
</h1>

<p align="center">
    <img alt="License: MIT" src="https://img.shields.io/apm/l/vim-mode.svg?style=flat">
    <a href="https://github.com/ambv/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/perf.svg?style=flat" />
    <img src="https://travis-ci.com/MisterBianco/Wire.svg?branch=master" />
    <a href="https://codecov.io/gh/MisterBianco/Wire">
        <img src="https://codecov.io/gh/MisterBianco/Wire/branch/master/graph/badge.svg" />
    </a>
    <a href="https://www.codefactor.io/repository/github/misterbianco/wire">
        <img src="https://www.codefactor.io/repository/github/misterbianco/wire/badge" alt="CodeFactor" />
    </a>
</p>

Wire is a python wrapper around selenium to make writing web tests easier and safer.

This framework is built for python 3.7+

---

### Installation

Environment with python3.7 and [Poetry](https://github.com/sdispater/poetry)

```bash
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
$ poetry install
$ poetry run pytest tests/
```

---

# Run locally

Simple just define a browser instance

```python3
with Chrome() as b:
    b.get("https://google.com")
```

# Run remote

Also simple :snake:

<img src="assets/chrome.png" />

### Install Drivers

#### Chrome Driver

MAC

```bash
$ brew tap homebrew/cask && brew cask install chromedriver
```

LINUX

```bash
$ sudo ./install_chromedriver.sh
```

#### Firefox Driver

MAC

```bash
$ brew install geckodriver
```

LINUX

```bash
$ sudo ./install_gecko.sh
```

---

