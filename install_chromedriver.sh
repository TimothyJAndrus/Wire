#!/bin/bash

export LATEST_CHROMEDRIVER="$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)"
curl -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${LATEST_CHROMEDRIVER}/chromedriver_linux64.zip"
unzip /tmp/chromedriver.zip -d "/usr/local/bin/"
