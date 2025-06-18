# GEO AI Optimizer

An AI-powered content optimization and distribution platform that helps optimize content for AI assistants and search engines.

## Features

- Content optimization for AI assistants
- Entity extraction and linking
- Schema generation
- Multi-platform content distribution
- Analytics and insights
- Error handling and logging
- Comprehensive testing suite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/automated-content-optimizer.git
cd automated-content-optimizer
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

1. Start the server:
```bash
uvicorn src.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite:
```bash
pytest tests/ --cov=src
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Run code quality checks:
```bash
black .
flake8 .
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI
- spaCy
- Transformers
- Sentence Transformers
- And all other open-source libraries used in this project
