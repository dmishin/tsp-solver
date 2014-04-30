test:
	python -m unittest discover -s tests

test2:
	python2 -m unittest discover -s tests

perf:
	PYTHONPATH=.:$(PYTHONPATH) python tests/perftest.py

deb:
	fakeroot checkinstall --pkgname=python-tsp-solver --pkgversion=0.1 --install=no -y python setup.py install

.PHONY: test test2 perf deb
