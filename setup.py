"""Setup configuration for the content optimizer package."""

from setuptools import setup, find_packages

setup(
    name="content-optimizer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "nltk>=3.8.1",
        "transformers>=4.30.0",
        "moviepy>=1.0.3",
        "librosa>=0.10.0",
        "pillow>=10.0.0",
        "gradio>=3.50.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "requests>=2.31.0",
        "python-multipart>=0.0.6",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "isort>=5.12.0",
        ],
    },
) 