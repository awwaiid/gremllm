.PHONY: help install install-dev lint format fix type-check test clean build upload-test upload

help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  install-dev  Install package with dev dependencies"
	@echo "  lint         Run linting (ruff check)"
	@echo "  format       Run formatting (ruff format)"
	@echo "  fix          Fix all linting issues and format code"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  test         Run tests (pytest)"
	@echo "  build        Build package for distribution"
	@echo "  upload-test  Upload to Test PyPI"
	@echo "  upload       Upload to PyPI"
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

fix:
	ruff check --fix .
	ruff format .

type-check:
	mypy .

test:
	pytest

build:
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

