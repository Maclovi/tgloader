ruff check
mypy
bandit -c pyproject.toml -r loader
semgrep scan --config auto --error
codespell
