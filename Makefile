VENV=./ve
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip


$(VENV):
	virtualenv $(VENV) -p python3.5

build-html: $(VENV)
	tar -cvf backup.tar docs/source docs/build docs/Makefile
	rm -rf docs/
	tar -xvf backup.tar
	rm backup.tar
	$(PIP) install sphinx sphinx-autobuild
	$(MAKE) -C docs/ clean && $(MAKE) -C docs/ html
	cp -r docs/build/html/. docs/

clean-virtualenv:
	rm -rf $(VENV)
