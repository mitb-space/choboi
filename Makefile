
PYTHON=./venv/bin/python3
PID=choboi.pid

run:
	$(PYTHON) choboi.py

start:
	$(PYTHON) choboi.py > /dev/null 2>&1 & echo $$! > $(PID)

kill:
	kill $$(cat $(PID))
