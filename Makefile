bootstrap:
	pip install -r requirements.txt

lint:
	flake8 src test

test:
	PYTHONPATH=src python -m unittest discover -s test -v

serve:
	PYTHONPATH=src python src/skyserve.py

.PHONY: bootstrap lint test
