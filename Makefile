.PHONY: docs test coverage clean install format lint build publish check sdk-test-flow release

# Variables
PYTHON = poetry run python
PYTEST = poetry run pytest
SPHINX_BUILD = poetry run sphinx-build

# Default target
all: test docs

# Build documentation
docs:
	@echo "Building documentation..."
	$(SPHINX_BUILD) -b html docs docs/_build/html

# Run tests
test:
	@echo "Running tests..."
	$(PYTEST)

# Run tests with coverage
coverage:
	@echo "Running tests with coverage..."
	$(PYTEST) --cov=my_cache_sdk --cov-report=html

# Clean up build artifacts
clean:
	@echo "Cleaning up..."
	rm -rf docs/_build
	rm -rf .pytest_cache
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Install dependencies
install:
	@echo "Installing dependencies..."
	poetry install

# Format code and fix imports
format:
	@echo "Formatting code and fixing imports..."
	poetry run black .
	poetry run isort .

# Check code style
lint:
	@echo "Linting code..."
	poetry run flake8 src tests
	poetry run black --check .
	poetry run isort --check-only .

# Build the package
build:
	@echo "Building package..."
	poetry build

# Publish the package to PyPI
publish:
	@echo "Publishing package..."
	poetry publish

# Run all checks (tests, coverage, lint)
check: test coverage lint

# Run SDK install and test flow
sdk-test-flow:
	@echo "Running SDK install and test flow..."
	$(PYTHON) test_sdk_flow.py

# Check code complexity
complexity:
	@echo "Checking code complexity..."
	poetry run radon cc src -a -nc

# Serve documentation locally
serve-docs: docs
	@echo "Serving documentation..."
	@cd docs/_build/html && python -m http.server $(PORT)

# Release a new version
release:
	@echo "Releasing new version..."
	@echo "New version number:"
	@read VERSION && \
	poetry version $$VERSION && \
	git add pyproject.toml && \
	git commit -m "Bump version to $$VERSION" --no-verify && \
	git tag v$$VERSION && \
	git push origin master --no-verify && \
	git push origin v$$VERSION --no-verify && \
	make build && \
	make publish && \
	make docs