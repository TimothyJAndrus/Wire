install:
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

init:
    poetry install

test:
    poetry run pytest tests/ --headless -s -x -n 2
