# Contributing Guide

Thank you for considering contributing to the Automated Content Optimizer! This document outlines the process and guidelines for contributing to our project.

## Code of Conduct

Please read and follow our Code of Conduct to keep our community respectful and inclusive.

## How to Contribute

1. **Fork the Repository**
   - Fork the repository on GitHub
   - Clone your fork locally

2. **Set Up Development Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write clear, concise commit messages
   - Follow our coding standards
   - Add tests for new features
   - Update documentation as needed

5. **Test Your Changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code formatting
   black .
   flake8 .
   mypy .
   ```

6. **Submit a Pull Request**
   - Push your changes to your fork
   - Create a pull request from your fork to our main repository
   - Describe your changes in detail
   - Reference any related issues

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions and classes
- Keep functions focused and concise
- Use meaningful variable and function names

### Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use pytest fixtures and parametrize when appropriate

### Documentation

- Update relevant documentation
- Add docstrings to new code
- Include examples for new features
- Keep README.md up to date

### Commit Messages

Follow the conventional commits specification:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test updates
- chore: Maintenance tasks

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation with details of changes if needed
3. The PR must pass all CI checks
4. The PR must be reviewed by at least one maintainer
5. The PR should be rebased on the latest main branch

## Getting Help

- Open an issue for bugs or feature requests
- Join our community discussions
- Contact maintainers for guidance

## License

By contributing, you agree that your contributions will be licensed under the project's license. 