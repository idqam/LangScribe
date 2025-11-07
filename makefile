TMP ?= $(abspath tmp)

RUFF_CHECK_FLAGS = --quiet
RUFF_FORMAT_FLAGS = --quiet


DIRS = AIWorker WebServer

.PHONY: format
format:
	uv run ruff format $(RUFF_FORMAT_FLAGS) $(DIRS)

.PHONY: check
check:
	uv run ruff check $(RUFF_CHECK_FLAGS) --fix $(DIRS)

.PHONY: mypy
mypy:
	uv run mypy $(DIRS)

.PHONY: vulture
vulture:
	uv run vulture $(DIRS)

.PHONY: ci
ci:
	uv run ruff check $(DIRS)  # No --fix in CI
	uv run ruff format --check $(DIRS)  # Check only, don't format
	uv run mypy $(DIRS)
	uv run vulture $(DIRS)

.PHONY: pre-commit
pre-commit:
	uv run pre-commit install 

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  format      - Format code with ruff
	@echo "  check       - Lint and fix with ruff
	@echo "  mypy        - Type check with mypy"
	@echo "  vulture     - Find dead code with vulture
	@echo "  pre-commit  - Format + lint (run before commit)"
	@echo "  ci          - Run checks without auto-fix (for CI/CD)"