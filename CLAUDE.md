# CLAUDE.md

This file provides guidance for AI assistants working with this repository.

## Repository Overview

This is a Python project repository (`tylerhoth/test-repository`). It currently contains a minimal scaffold with a single application entry point.

## Project Structure

```
.
└── app.py          # Main application file (Python)
```

## Language and Runtime

- **Language**: Python
- **No package manager** configured (no `requirements.txt`, `pyproject.toml`, or `setup.py`)
- **No virtual environment** configuration present

## Build and Run

There is no build system. To run the application:

```sh
python app.py
```

## Testing

No test framework or test files are currently configured.

## Linting and Formatting

No linters or formatters are configured. When adding Python tooling, standard choices include:
- `ruff` or `flake8` for linting
- `black` or `ruff format` for formatting

## CI/CD

No CI/CD pipelines are configured.

## Dependencies

No external dependencies are declared.

## Git Conventions

- **Main branch**: `master`
- Commit messages should be concise and descriptive
- The repository uses SSH-based commit signing

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main application entry point |
