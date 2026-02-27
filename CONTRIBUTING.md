# Contributing to Voice Persona Engine

Thank you for your interest in contributing! This document provides guidelines for participating in the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/voice-persona-engine.git
   cd voice-persona-engine
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install in development mode with all dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Code Style

We follow these conventions:
- **Black** for code formatting (100 char line length)
- **Ruff** for linting (E, F, W, I, N rules)
- **Type hints** for function signatures

Before committing, run:
```bash
black persona tests
ruff check --fix .
```

### Testing

Write tests for all new features and bug fixes. Run tests before committing:
```bash
pytest tests/ -v
pytest tests/ --cov=persona  # With coverage
```

Tests are organized by module:
- `tests/test_engine.py` - PersonaEngine and Persona classes
- `tests/test_traits.py` - PersonaTraits and trait validation
- `tests/test_prompts.py` - Prompt generation and modifiers

### Documentation

- Keep docstrings clear and concise
- Use type hints for function parameters and return types
- Include examples in docstrings for public APIs
- Update README.md if adding new features

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit with clear messages:
   ```bash
   git commit -m "Add feature: clear description of what changed"
   ```
3. Run tests and lint checks:
   ```bash
   pytest tests/ -v
   ruff check .
   black --check persona tests
   ```
4. Push to your fork and submit a pull request on GitHub

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Include a clear description of changes
- Reference any related issues
- Ensure all tests pass and code is properly formatted
- Add tests for new functionality

## Reporting Issues

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Minimal code example if applicable

## Feature Requests

Feature requests are welcome! Please describe:
- The use case you're trying to solve
- Why you think it would be valuable
- Any potential implementation approaches

## Questions?

Open a GitHub issue or discussion for questions about the project.

---

Thank you for contributing to Voice Persona Engine!
