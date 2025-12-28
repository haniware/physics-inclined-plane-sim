# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python physics simulation project. The project is currently in its initial setup phase.

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Install development dependencies (when requirements-dev.txt exists)
pip install -r requirements-dev.txt
```

### Running the Application
```bash
# Run the main simulation (when main.py or similar exists)
python main.py

# Run a specific module
python -m <module_name>
```

### Testing
```bash
# Run all tests (when tests exist)
python -m pytest

# Run a specific test file
python -m pytest tests/test_<name>.py

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Code Quality
```bash
# Format code (if using black)
black .

# Lint code (if using pylint/flake8)
pylint *.py
flake8 .

# Type checking (if using mypy)
mypy .
```

## Project Structure

The project uses a Python virtual environment located in `.venv/`. Source code should be organized according to standard Python project conventions.

## Development Notes

- Python virtual environment: `.venv/`
- IDE: PyCharm
- Project is currently in initial setup phase
