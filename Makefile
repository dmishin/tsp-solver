test:
	python -m unittest discover -s tests

test2:
	python2 -m unittest discover -s tests

.PHONY: test test2
