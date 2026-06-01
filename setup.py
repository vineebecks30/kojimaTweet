"""Setup configuration for KojimaTweet package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kojima-tweet",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Analyze Hideo Kojima's movie review tweets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kojimaTweet",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tweepy>=4.14.0",
        "python-dotenv>=1.0.0",
        "cachetools>=5.3.0",
        "colorlog>=6.7.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "bandit>=1.7.5",
            "safety>=2.3.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "kojima-tweet=src.main:main",
        ],
    },
)

# Made with Bob
