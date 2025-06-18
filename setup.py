"""Setup configuration for the content optimizer package."""

from setuptools import setup, find_packages

setup(
    name="automated-content-optimizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "nltk",
        "spacy",
        "transformers",
        "sentence-transformers",
        "beautifulsoup4",
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "pytest-mock"
    ],
) 