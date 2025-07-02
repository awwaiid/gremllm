.PHONY: help install install-dev lint format type-check test clean pre-commit

help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  install-dev  Install package with dev dependencies"
	@echo "  lint         Run linting (ruff check)"
	@echo "  format       Run formatting (ruff format)"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  test         Run tests (pytest)"
	@echo "  clean        Clean build artifacts"
	@echo "  pre-commit   Install pre-commit hooks"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	ruff check .

format:
	ruff format .

type-check:
	mypy .

test:
	pytest

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

pre-commit:
	pre-commit install