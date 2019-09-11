SHELL=/bin/bash

.PHONY: all
all:
	@echo "I don't build anything yet."

venv: requirements.txt
	@rm -rf $@
	virtualenv $@ \
	&& . ./$@/bin/activate \
	&& pip install -r $<

.PHONY: webapp
webapp:
	$(MAKE) -C webapp

.PHONY: clean
clean:
	@rm -rf venv
	@$(MAKE) -C webapp clean
