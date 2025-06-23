# Makefile for Math Expert LLM Application Tests

.PHONY: help test test-unit test-integration test-performance test-fast test-coverage clean install-dev check-deps

# Default target
help:
	@echo "Math Expert LLM Application - Test Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  help              Show this help message"
	@echo "  install-dev       Install development dependencies"
	@echo "  check-deps        Check if test dependencies are installed"
	@echo "  test              Run all tests"
	@echo "  test-unit         Run unit tests only"
	@echo "  test-integration  Run integration tests only"
	@echo "  test-performance  Run performance/stress tests"
	@echo "  test-fast         Run fast tests (exclude performance)"
	@echo "  test-coverage     Run tests with detailed coverage report"
	@echo "  clean             Clean test artifacts"
	@echo "  lint              Run code linting"
	@echo "  format            Format code"
	@echo ""
	@echo "Examples:"
	@echo "  make test-unit           # Quick unit test run"
	@echo "  make test-coverage       # Full test run with coverage"
	@echo "  make test-performance    # Performance benchmarking"

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	poetry install --with dev

# Check if test dependencies are installed
check-deps:
	@echo "Checking test dependencies..."
	python tests/run_tests.py --check-deps

# Run all tests
test:
	@echo "Running all tests..."
	python tests/run_tests.py all

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	python tests/run_tests.py unit -v

# Run integration tests only
test-integration:
	@echo "Running integration tests..."
	python tests/run_tests.py integration -v

# Run performance tests
test-performance:
	@echo "Running performance tests..."
	python tests/run_tests.py performance -v

# Run fast tests (exclude slow performance tests)
test-fast:
	@echo "Running fast tests..."
	python tests/run_tests.py fast

# Run tests with detailed coverage
test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=85 -v

# Run tests in parallel
test-parallel:
	@echo "Running tests in parallel..."
	python tests/run_tests.py all -p

# Run specific test file
test-file:
	@echo "Usage: make test-file FILE=tests/unit/test_tools.py"
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE parameter is required"; \
		echo "Example: make test-file FILE=tests/unit/test_tools.py"; \
		exit 1; \
	fi
	python -m pytest $(FILE) -v

# Run tests with specific marker
test-marker:
	@echo "Usage: make test-marker MARKER=unit"
	@if [ -z "$(MARKER)" ]; then \
		echo "Error: MARKER parameter is required"; \
		echo "Example: make test-marker MARKER=unit"; \
		echo "Available markers: unit, integration, slow, aws, llm"; \
		exit 1; \
	fi
	python -m pytest -m $(MARKER) -v

# Clean test artifacts
clean:
	@echo "Cleaning test artifacts..."
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run code linting (if available)
lint:
	@echo "Running code linting..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ tests/; \
	else \
		echo "flake8 not found. Install with: poetry add --group dev flake8"; \
	fi
	@if command -v mypy >/dev/null 2>&1; then \
		mypy src/; \
	else \
		echo "mypy not found. Install with: poetry add --group dev mypy"; \
	fi

# Format code (if available)
format:
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black src/ tests/; \
	else \
		echo "black not found. Install with: poetry add --group dev black"; \
	fi
	@if command -v isort >/dev/null 2>&1; then \
		isort src/ tests/; \
	else \
		echo "isort not found. Install with: poetry add --group dev isort"; \
	fi

# Run tests continuously (watch mode)
test-watch:
	@echo "Running tests in watch mode..."
	@if command -v pytest-watch >/dev/null 2>&1; then \
		ptw tests/ src/; \
	else \
		echo "pytest-watch not found. Install with: poetry add --group dev pytest-watch"; \
		echo "Falling back to simple test run..."; \
		make test-fast; \
	fi

# Generate test report
test-report:
	@echo "Generating test report..."
	python -m pytest tests/ --cov=src --cov-report=html:htmlcov --cov-report=xml:coverage.xml --junit-xml=test-results.xml
	@echo "Reports generated:"
	@echo "  HTML Coverage: htmlcov/index.html"
	@echo "  XML Coverage: coverage.xml"
	@echo "  JUnit XML: test-results.xml"

# Debug specific test
debug-test:
	@echo "Usage: make debug-test TEST=tests/unit/test_tools.py::TestMathTools::test_sum_values_calculation"
	@if [ -z "$(TEST)" ]; then \
		echo "Error: TEST parameter is required"; \
		echo "Example: make debug-test TEST=tests/unit/test_tools.py::TestMathTools::test_sum_values_calculation"; \
		exit 1; \
	fi
	python -m pytest $(TEST) -v -s --pdb

# Setup development environment
setup-dev: install-dev
	@echo "Setting up development environment..."
	@echo "Creating .env file for local development..."
	@if [ ! -f src/env/local/.env ]; then \
		echo "DEBUG=True" > src/env/local/.env; \
		echo "ENVIRONMENT=local" >> src/env/local/.env; \
		echo "AWS_REGION=us-east-1" >> src/env/local/.env; \
		echo "Local .env file created at src/env/local/.env"; \
		echo "Please update AWS credentials as needed."; \
	else \
		echo "Local .env file already exists."; \
	fi
	@echo "Development environment setup complete!"

# Quality check (lint + format + test)
quality: format lint test-fast
	@echo "Quality check completed!"

# Full CI pipeline
ci: install-dev quality test-coverage
	@echo "CI pipeline completed!"

# Show test structure
show-structure:
	@echo "Test structure:"
	@find tests/ -name "*.py" | sort | sed 's|^|  |'
