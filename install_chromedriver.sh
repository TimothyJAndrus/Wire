#!/bin/bash

export LATEST_CHROMEDRIVER="$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)"
curl -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${LATEST_CHROMEDRIVER}/chromedriver_linux64.zip"
mkdir "/usr/local/bin/chromedriver"
unzip /tmp/chromedriver.zip -d "/usr/local/bin/chromedriver"
export PATH="/usr/local/bin/chromedriver:${PATH}"
chromedriver --version
