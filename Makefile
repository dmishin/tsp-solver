test:
	python -m unittest discover -s tests

test2:
	python2 -m unittest discover -s tests

perf:
	PYTHONPATH=.:$(PYTHONPATH) python tests/perftest.py

checkinstall:
	checkinstall --pkgname=python-tsp-solver --pkgversion=0.4 --install=yes -y python setup.py install


demo:
	PYTHONPATH=.:$(PYTHONPATH) ./bin/tsp_demo -p ring

.PHONY: test test2 perf deb demo checkinstall
