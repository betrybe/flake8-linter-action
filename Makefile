install:
	python3 -m pip install -r requirements.txt

flake8:
	python3 -m flake8 --append-config=setup.cfg

test:
	python3 -m pytest -s

build:
	docker build . -t 'flake8_linter_action'
