VERSION=$(shell git describe --tags 2> /dev/null || echo '0.0.0')
PYTHON=./venv/bin/python3
PID=choboi.pid

run:
	$(PYTHON) choboi.py

start:
	$(PYTHON) choboi.py > /dev/null 2>&1 & echo $$! > $(PID)

kill:
	kill $$(cat $(PID))
