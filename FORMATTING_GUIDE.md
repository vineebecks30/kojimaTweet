# Code Formatting Guide

## Black Formatting Required

This project uses [Black](https://black.readthedocs.io/) for code formatting to ensure consistent code style.

## Setup

Install Black and other development tools:

```bash
pip install -r requirements.txt
```

Or install just the dev dependencies:

```bash
pip install black flake8 mypy pytest
```

## Format Code

### Format all Python files:

```bash
black src/ tests/ config/
```

### Check formatting without making changes:

```bash
black --check src/ tests/ config/
```

### Format specific file:

```bash
black src/main.py
```

## Configuration

Black configuration is in `pyproject.toml`:

- Line length: 88 characters (Black default)
- Target Python versions: 3.8, 3.9, 3.10, 3.11
- Excludes: .eggs, .git, .venv, build, dist

## Pre-commit Hook (Recommended)

Install pre-commit hook to automatically format code before commits:

```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.10
```

## CI/CD

The GitHub Actions workflow automatically checks formatting:

- Runs `black --check` on all Python files
- Fails if any files need formatting
- Run `black src/ tests/ config/` locally before pushing

## Other Code Quality Tools

### Flake8 (Linting)
```bash
flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503
```

### MyPy (Type Checking)
```bash
mypy src/ --ignore-missing-imports
```

### Bandit (Security)
```bash
bandit -r src/ -ll
```

## Quick Fix

If CI fails due to formatting, run:

```bash
# Format all files
black src/ tests/ config/

# Verify
black --check src/ tests/ config/

# Commit and push
git add .
git commit -m "Apply Black formatting"
git push
```

## IDE Integration

### VS Code

Install the Python extension and add to `settings.json`:

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true
}
```

### PyCharm

1. Go to Settings → Tools → Black
2. Enable "On save"
3. Set path to Black executable

## Common Issues

### Issue: "would reformat X files"

**Solution**: Run `black src/ tests/ config/` to format the files.

### Issue: Black not found

**Solution**: Install Black: `pip install black`

### Issue: Different formatting on different machines

**Solution**: Ensure same Black version across all environments. Pin version in requirements.txt.

## Best Practices

1. **Always format before committing**
2. **Use pre-commit hooks** for automatic formatting
3. **Keep Black version consistent** across team
4. **Don't fight Black** - accept its formatting decisions
5. **Format entire files**, not just changed lines

## Resources

- [Black Documentation](https://black.readthedocs.io/)
- [Black Playground](https://black.vercel.app/)
- [PEP 8 Style Guide](https://pep8.org/)