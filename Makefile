.PHONY: help install format lint test clean build run docker-build docker-run

help:
	@echo "KojimaTweet - Available Commands"
	@echo "================================"
	@echo "install       - Install dependencies"
	@echo "format        - Format code with Black"
	@echo "lint          - Run linting checks"
	@echo "test          - Run tests with coverage"
	@echo "clean         - Clean build artifacts"
	@echo "build         - Build package"
	@echo "run           - Run the application"
	@echo "docker-build  - Build Docker image"
	@echo "docker-run    - Run with Docker Compose"

install:
	pip install -r requirements.txt

format:
	black src/ tests/ config/
	@echo "✅ Code formatted successfully"

lint:
	@echo "Running Black check..."
	black --check src/ tests/ config/
	@echo "Running Flake8..."
	flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503
	@echo "Running MyPy..."
	mypy src/ --ignore-missing-imports
	@echo "✅ All linting checks passed"

test:
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "✅ Tests completed"

security:
	@echo "Running Bandit security scan..."
	bandit -r src/ -ll
	@echo "Checking dependencies for vulnerabilities..."
	safety check
	@echo "✅ Security checks completed"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf logs/*.log
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned build artifacts"

build: clean
	python -m build
	@echo "✅ Package built successfully"

run:
	python -m src.main

docker-build:
	docker build -t kojima-tweet:latest .
	@echo "✅ Docker image built"

docker-run:
	docker-compose up -d
	@echo "✅ Application running in Docker"

docker-stop:
	docker-compose down
	@echo "✅ Docker containers stopped"

docker-logs:
	docker-compose logs -f

all: format lint test
	@echo "✅ All checks passed!"

# Made with Bob
