install:
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

init:
    poetry install

test:
    pytest tests/ --headless -s
