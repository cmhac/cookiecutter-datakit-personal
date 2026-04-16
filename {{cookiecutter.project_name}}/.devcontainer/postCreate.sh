#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed or not on PATH." >&2
  exit 1
fi

# In CI, always use home directory for uv cache to avoid permission issues
# with UID remapping in devcontainers/ci action
if [[ -n "${CI:-}" ]]; then
  export UV_PYTHON_INSTALL_DIR="${HOME}/.uv-python"
  echo "Running in CI, using ${UV_PYTHON_INSTALL_DIR} for uv Python installations" >&2
fi
if [[ ! -f pyproject.toml ]]; then
  echo "Expected pyproject.toml in workspace root (${repo_root}), but it was not found." >&2
  echo "This usually means the workspace content synced into the container is incomplete." >&2
  echo "Current directory listing:" >&2
  ls -la >&2 || true
  exit 1
fi

uv sync --dev

uv run pre-commit install --install-hooks || true

# Set up AWS config for datakit to use IAM role credentials
# This is needed in the devcontainer where we use IAM roles instead of traditional credentials
mkdir -p ~/.aws
cat > ~/.aws/config <<'EOF'
[default]
credential_source = Ec2InstanceMetadata
EOF

echo "AWS config created for datakit to use IAM role credentials"
