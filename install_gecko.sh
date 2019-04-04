#!/bin/bash

curl -L -s -o /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

mkdir "${HOME}/geckodriver"
tar -xvzf /tmp/geckodriver.tar.gz -C "${HOME}/geckodriver"
