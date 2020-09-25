.PHONY: help
help:
	@echo 'Makefile for `local-dd-agent` project'
	@echo ''
	@echo 'Usage:'
	@echo '   make build    Build Docker container with `local-dd-agent`'
	@echo '   make run      Run Docker container with `local-dd-agent` in the foreground'
	@echo ''

.PHONY: build
build:
	docker build \
	  --tag dhermes/local-dd-agent:latest \
	  --file docker/datadog.Dockerfile \
	  .

.PHONY: run
run:
	@./_bin/run.sh
