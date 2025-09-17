# Lightweight Makefile for MCP Docassemble workflows

PYTHON ?= python
PACKAGE := mcp_docassemble
IMAGE := ghcr.io/$(shell whoami)/mcp-docassemble
TAG ?= latest

.PHONY: help install dev-install test test-all lint fmt docker-build docker-run clean

help:
	@echo "Available targets:"
	@echo "  install        Install the package with runtime dependencies"
	@echo "  dev-install    Install the package with development extras"
	@echo "  test           Run the offline sanity checks"
	@echo "  test-all       Run the full test suite (requires live Docassemble)"
	@echo "  lint           Run formatting and static checks"
	@echo "  fmt            Format code with black and isort"
	@echo "  docker-build   Build the production Docker image"
	@echo "  docker-run     Run the Docker image with local environment variables"
	@echo "  clean          Remove Python build artefacts"

install:
	$(PYTHON) -m pip install .

dev-install:
	$(PYTHON) -m pip install '.[dev]'

test:
	pytest tests/test_sanity.py -v

test-all:
	MCP_DOCASSEMBLE_LIVE_TESTS=1 pytest -v

lint:
	black --check src tests
	isort --check-only src tests
	mypy src

fmt:
	black src tests
	isort src tests

docker-build:
	docker build -t $(IMAGE):$(TAG) .

docker-run:
	docker run --rm \
		-e DOCASSEMBLE_BASE_URL \
		-e DOCASSEMBLE_API_KEY \
		$(IMAGE):$(TAG)

clean:
	rm -rf build dist *.egg-info
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
