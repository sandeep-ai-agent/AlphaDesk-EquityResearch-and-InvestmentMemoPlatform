#!/usr/bin/env bash
set -euo pipefail

# Install repository support for Git Large File Storage.
sudo apt-get update
sudo apt-get install -y --no-install-recommends git-lfs
git lfs install --local

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