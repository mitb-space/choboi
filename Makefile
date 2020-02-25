VERSION=$(shell git describe --tags 2> /dev/null || echo '0.0.0')
PYTHON=./venv/bin/python3
PID=choboi.pid
APP_NAME=choboi
DOCKER_REPO=davidharrigan

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


bootstrap:
	python3 -m venv ./venv
	./venv/bin/pip install -r requirements/test.txt

lint:
	pylint --rcfile=.pylintrc ./choboi

test:
	# pytest

run:
	$(PYTHON) choboi.py

start:
	$(PYTHON) choboi.py > /dev/null 2>&1 & echo $$! > $(PID)

kill:
	kill $$(cat $(PID))

docker/build:
	docker build -t $(APP_NAME) .

docker/release: docker/build docker/tag
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

	@echo 'publish latest to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):latest

docker/tag: docker/tag-latest docker/tag-version

docker/tag-latest:
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

docker/tag-version:
	@echo 'create tag $(VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)
