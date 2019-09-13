SHELL=/bin/bash

.PHONY: all
all:
	@echo "Nothing to do for all."

venv: requirements.txt requirements-dev.txt
	@rm -rf $@
	virtualenv --python=python3.7 $@ \
	&& . ./$@/bin/activate \
	&& pip install `cat $+`

.PHONY: webapp
webapp:
	@$(MAKE) -C webapp

.PHONY: clean
clean: clean-webapp clean-build
	@echo Cleaned.

.PHONY: clean-venv
clean-venv:
	@rm -rf venv

.PHONY: clean-build
clean-build:
	@rm -rf .build

.PHONY: clean-webapp
clean-webapp:
	@$(MAKE) -C webapp clean
