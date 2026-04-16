"""Post-generation hook for project bootstrap tasks."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str]) -> None:
    """Run a command and fail fast on error."""
    print(f"[cookiecutter] Running: {' '.join(command)}")
    subprocess.run(command, check=True)


def ensure_command_exists(command_name: str) -> None:
    """Ensure required command is available on PATH."""
    if shutil.which(command_name) is None:
        print(f"[cookiecutter] Required command not found: {command_name}")
        sys.exit(1)


def main() -> None:
    """Initialize git repo and bootstrap project dependencies/hooks."""
    project_root = Path.cwd()
    print(f"[cookiecutter] Bootstrapping project in: {project_root}")

    ensure_command_exists("git")
    ensure_command_exists("uv")

    if (project_root / ".git").exists():
        print("[cookiecutter] Git repo already exists, skipping: git init")
    else:
        run_command(["git", "init"])

    run_command(["uv", "sync"])
    run_command(["uv", "run", "pre-commit", "install"])
    print("[cookiecutter] Bootstrap complete")


if __name__ == "__main__":
    main()
