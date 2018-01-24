VENV=./ve
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
FLASK=$(VENV)/bin/flask
FLAKE8=$(VENV)/bin/flake8
CODEGEN_VERSION=2.3.1
CODEGEN=java -jar swagger-codegen-cli-$(CODEGEN_VERSION).jar generate
ACCESS_CONTROL_CLIENT_DIR=access_control_client
DB_NAME=access_control
DB_USER=access_control

# Colours.
CLEAR=\033[0m
RED=\033[0;31m
GREEN=\033[0;32m
CYAN=\033[0;36m

.SILENT: docs-build
.PHONY: check

help:
	@echo "usage: make <target>"
	@echo "    $(CYAN)build-virtualenv$(CLEAR): Creates virtualenv directory, 've/', in project root."
	@echo "    $(CYAN)clean-virtualenv$(CLEAR): Deletes 've/' directory in project root."
	@echo "    $(CYAN)docs-build$(CLEAR): Build documents and place html output in docs root."
	@echo "    $(CYAN)mock-access-control-api$(CLEAR): Starts Prism mock server for the Access Control API."
	@echo "    $(CYAN)validate-swagger$(CLEAR): Check Swagger spec for errors."
	@echo "    $(CYAN)access-control-client$(CLEAR): Generate a client for the Access Control API."
	@echo "    $(CYAN)access-control-api$(CLEAR): Generate a Flask server for the Access Control API."

$(VENV):
	@echo "$(CYAN)Initialise base ve...$(CLEAR)"
	virtualenv $(VENV) -p python3.5
	@echo "$(GREEN)DONE$(CLEAR)"

# Creates the virtual environment.
build-virtualenv: $(VENV)
	@echo "$(CYAN)Building virtualenv...$(CLEAR)"
	# TODO: Depending on project type, requirements will need to be installed here.
	@echo "$(GREEN)DONE$(CLEAR)"

# Deletes the virtual environment.
clean-virtualenv:
	@echo "$(CYAN)Clearing virtualenv...$(CLEAR)"
	rm -rf $(VENV)
	@echo "$(GREEN)DONE$(CLEAR)"

# Build sphinx docs, then move them to docs/ root for GitHub Pages usage.
docs-build:  $(VENV)
	@echo "$(CYAN)Installing Sphinx requirements...$(CLEAR)"
	$(PIP) install sphinx sphinx-autobuild
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Backing up docs/ directory content...$(CLEAR)"
	tar -cvf backup.tar docs/source docs/Makefile
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Clearing out docs/ directory content...$(CLEAR)"
	rm -rf docs/
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Restoring base docs/ directory content...$(CLEAR)"
	tar -xvf backup.tar
	@echo "$(GREEN)DONE$(CLEAR)"
	# Remove the tar file.
	rm backup.tar
	# Actually make html from index.rst
	@echo "$(CYAN)Running sphinx command...$(CLEAR)"
	$(MAKE) -C docs/ clean html SPHINXBUILD=../$(VENV)/bin/sphinx-build
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Moving build files to docs/ root...$(CLEAR)"
	cp -r docs/build/html/. docs/
	rm -rf docs/build/
	@echo "$(GREEN)DONE$(CLEAR)"

swagger-codegen-cli-$(CODEGEN_VERSION).jar:
	wget https://oss.sonatype.org/content/repositories/releases/io/swagger/swagger-codegen-cli/$(CODEGEN_VERSION)/swagger-codegen-cli-$(CODEGEN_VERSION).jar

prism:
	curl -L https://github.com/stoplightio/prism/releases/download/v0.6.21/prism_linux_amd64 -o prism
	chmod +x prism

mock-access-control-api: prism
	./prism run --mockDynamic --list -s swagger/access_control.yml -p 8010

validate-swagger: prism
	@./prism validate -s swagger/access_control.yml && echo "The Swagger spec contains no errors"

$(FLAKE8): $(VENV)
	$(PIP) install flake8

# Generate the client code to interface with Access Control
access-control-client: swagger-codegen-cli-$(CODEGEN_VERSION).jar
	@echo "$(CYAN)Generating the client for the Access Control API...$(CLEAR)"
	$(CODEGEN) -l python -i swagger/access_control.yml -o /tmp/$(ACCESS_CONTROL_CLIENT_DIR)
	cp -r /tmp/$(ACCESS_CONTROL_CLIENT_DIR)/swagger_client* $(ACCESS_CONTROL_CLIENT_DIR)
	rm -rf /tmp/$(ACCESS_CONTROL_CLIENT_DIR)

# Generate the flask server code for Access Control
access-control-api: swagger-codegen-cli-$(CODEGEN_VERSION).jar validate-swagger
	@echo "$(CYAN)Generating flask server for the Access Control API...$(CLEAR)"
	$(CODEGEN) -i swagger/access_control.yml -l python-flask -o .

runserver: $(VENV)
	@echo "$(CYAN)Firing up server...$(CLEAR)"
	$(PYTHON) -m swagger_server

check: $(FLAKE8)
	$(FLAKE8)

database:
	sql/create_database.sh $(DB_NAME) $(DB_USER) | sudo -u postgres psql -f -

makemigrations: $(VENV)
	@echo "$(CYAN)Creating migrating...$(CLEAR)"
	FLASK_APP=core_user_data_store/models.py $(FLASK) db migrate -d core_user_data_store/migrations

migrate: $(VENV)
	@echo "$(CYAN)Applying migrations to DB...$(CLEAR)"
	FLASK_APP=core_user_data_store/models.py $(FLASK) db upgrade -d core_user_data_store/migrations
