# Project name (adjust as needed)
PROJECT_NAME = twitter-agent

# Python interpreter (adjust if needed)
PYTHON = python3

# Virtual environment directory (adjust if needed)
VENV_DIR =.venv

# Source files (adjust as needed)
SOURCES = $(wildcard *.py)  # All.py files in the current directory
# Or specify them explicitly:
# SOURCES = main.py module1.py module2.py

# Tests (adjust as needed)
TESTS = tests/test_*.py

# Create virtual environment
$(VENV_DIR)/bin/activate:
        python3 -m venv $(VENV_DIR)

# Activate virtual environment (more convenient to just type `make venv`)
venv: $(VENV_DIR)/bin/activate
        @echo "Virtual environment activated."

# Install dependencies
install: venv
        $(VENV_DIR)/bin/pip install -r requirements.txt

# Run tests
test: venv
        $(VENV_DIR)/bin/python -m pytest $(TESTS)

# Run tests with coverage
coverage: venv
        $(VENV_DIR)/bin/coverage run -m pytest $(TESTS)
        $(VENV_DIR)/bin/coverage report

# Run the main application
run: venv
        $(VENV_DIR)/bin/python main.py  # Replace main.py with your main script

# Clean up (remove virtual environment, pycache, etc.)
clean:
        rm -rf $(VENV_DIR)
        rm -rf __pycache__ *.pyc *.pyd
        rm -rf.pytest_cache.coverage htmlcov
        rm -rf dist build *.egg *.whl *.tar.gz  # For distribution files

# Distribution (create packages)
dist: venv
        $(VENV_DIR)/bin/python setup.py sdist bdist_wheel

# Help (print available targets)
help:
        @echo "Available targets:"
        @echo "  venv:     Create and activate virtual environment"
        @echo "  install:  Install dependencies"
        @echo "  test:     Run tests"
        @echo "  coverage: Run tests with coverage"
        @echo "  run:      Run the main application"
        @echo "  clean:    Clean up"
        @echo "  dist:     Create distribution packages"
        @echo "  help:     Print this help message".PHONY: venv install test coverage run clean dist help # Declare phony targets