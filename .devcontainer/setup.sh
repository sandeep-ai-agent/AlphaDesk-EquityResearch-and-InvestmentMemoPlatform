#!/usr/bin/env bash
set -euo pipefail

# Install the same uv version used to initialize this project.
curl -LsSf https://astral.sh/uv/0.13.1/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

# Prepare the project interpreter and locked environment.
uv python install 3.11
uv sync --locked

# Show the environment selected for project commands.
uv --version
uv run python --version
uv run python -c "import sys; print(sys.executable)"