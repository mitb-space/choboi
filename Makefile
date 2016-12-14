
PYTHON=./venv/bin/python3

run:
	$(PYTHON) choboi.py

run-background:
	$(PYTHON) choboi.py > /dev/null 2>&1 &
	
