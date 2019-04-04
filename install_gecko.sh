#!/bin/bash

curl -L -s -o /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

mkdir "/usr/local/bin/geckodriver"
tar -xvzf /tmp/geckodriver.tar.gz -C "/usr/local/bin/geckodriver"
export PATH="/usr/local/bin/geckodriver:${PATH}"
geckodriver --version
