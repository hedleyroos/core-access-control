VENV=./ve
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip


$(VENV):
	virtualenv $(VENV) -p python3.5

create-virtualenv:
	$(VENV)

clean-virtualenv:
	rm -rf $(VENV)
