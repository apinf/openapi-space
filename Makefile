install-ci:
	pip install -r requirements/ci.txt

lint:
	pytest --flake8

test: lint
	py.test
