test:
	python -m unittest discover -s tests

test2:
	python2 -m unittest discover -s tests

perf:
	PYTHONPATH=.:$(PYTHONPATH) python3 tools/perftest.py
	PYTHONPATH=.:$(PYTHONPATH) python2 tools/perftest.py

.PHONY: test test2 perf
