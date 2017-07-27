all: test

install-ci:
	pip install -r requirements/ci.txt

install-local:
	pip install -r requirements/local.txt

debug:
	py.test --pudb

lint:
	pytest --flake8

test: lint
	py.test

setup:
	bash scripts/setup.sh

start:
	bash scripts/start.sh

docker-build:
	bash scripts/docker-build.sh

docker-push:
	bash scripts/docker-push.sh
