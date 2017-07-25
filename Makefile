install-ci:
	pip install -r requirements/ci.txt

install-local:
	pip install -r requirements/local.txt

lint:
	pytest --flake8

test: lint
	py.test
