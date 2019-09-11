SHELL=/bin/bash

all: node_modules
	npm run build

node_modules: package.json
	@rm -rf $@
	npm install

.PHONY: clean
clean:
	@rm -rf .build node_modules
