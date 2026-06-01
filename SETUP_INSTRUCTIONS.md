# Setup Instructions for KojimaTweet

## ⚠️ IMPORTANT: Code Formatting Required

The Python source files in this project need to be formatted with Black before the CI/CD pipeline will pass. This is a **required step** before committing code.

## Quick Setup (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including Black for code formatting.

### Step 2: Format Code with Black

**THIS IS REQUIRED** - Run this command to format all Python files:

```bash
black --target-version py310 src/ tests/ config/
```

Or use the Makefile:

```bash
make format
```

Expected output:
```
reformatted src/main.py
reformatted src/api/twitter_client.py
reformatted src/analyzers/movie_analyzer.py
... (12 files total)
All done! ✨ 🍰 ✨
12 files reformatted, 2 files left unchanged.
```

### Step 3: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Twitter API bearer token
nano .env  # or use your preferred editor
```

Add your Twitter API credentials:
```env
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
```

## Verify Setup

Run these commands to verify everything is set up correctly:

```bash
# 1. Check formatting (should pass after Step 2)
black --check --target-version py310 src/ tests/ config/

# 2. Run tests
make test
# OR
pytest

# 3. Run the application
make run
# OR
python -m src.main
```

## Why Black Formatting is Required

Black is an opinionated Python code formatter that ensures consistent code style across the project. The CI/CD pipeline checks that all code is properly formatted before allowing merges.

**Benefits:**
- Consistent code style
- No debates about formatting
- Automatic formatting
- Better code reviews (focus on logic, not style)

## Common Issues

### Issue: "would reformat X files"

This means the files need formatting. Run:
```bash
make format
```

### Issue: "black: command not found"

Black is not installed. Run:
```bash
pip install black
```

### Issue: "Python 3.11 cannot parse code formatted for Python 3.10"

This is expected. The project targets Python 3.10. The formatting command includes `--target-version py310` to handle this.

## Optional: Pre-commit Hooks

For automatic formatting before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Now Black will run automatically before each commit
```

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Build the image
docker-compose build

# Run the application
docker-compose up
```

Note: Docker will handle formatting internally, but you should still format code locally for development.

## Full Development Setup

For a complete development environment:

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Install pre-commit hooks
pip install pre-commit
pre-commit install

# 3. Format code
make format

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Run tests
make test

# 6. Run application
make run
```

## Makefile Commands

The project includes a Makefile for common tasks:

```bash
make help          # Show all available commands
make install       # Install dependencies
make format        # Format code with Black ⭐ REQUIRED
make lint          # Run linting checks
make test          # Run tests with coverage
make security      # Run security scans
make run           # Run the application
make docker-build  # Build Docker image
make docker-run    # Run with Docker Compose
make all           # Format, lint, and test
```

## Next Steps

After completing the setup:

1. ✅ Format code with Black (required)
2. ✅ Configure .env file
3. ✅ Run tests to verify
4. ✅ Run the application
5. ✅ Read README.md for usage instructions

## Getting Help

- **README.md**: User guide and usage examples
- **FORMATTING_GUIDE.md**: Detailed Black formatting guide
- **ANALYSIS_AND_IMPROVEMENTS.md**: Technical details
- **IMPLEMENTATION_SUMMARY.md**: Complete implementation overview

## Summary

**Required Steps:**
1. `pip install -r requirements.txt`
2. `make format` or `black --target-version py310 src/ tests/ config/`
3. `cp .env.example .env` and add your API token

**Verify:**
```bash
black --check --target-version py310 src/ tests/ config/
make test
make run
```

That's it! You're ready to use KojimaTweet. 🎬