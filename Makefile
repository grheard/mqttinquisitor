SHELL=/bin/bash

venv: requirements.txt
	@rm -rf $@
	virtualenv $@ \
	&& . ./$@/bin/activate \
	&& pip install -r $<

.PHONY: clean
clean:
	@rm -rf venv
