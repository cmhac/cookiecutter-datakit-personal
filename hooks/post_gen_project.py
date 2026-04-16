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


def has_existing_commit() -> bool:
    """Return True if the current repository already has commits."""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def create_initial_commit() -> None:
    """Create an initial commit after project bootstrap completes."""
    if has_existing_commit():
        print("[cookiecutter] Existing commit detected, skipping initial commit")
        return

    run_command(["git", "add", "-A"])

    try:
        run_command(["git", "commit", "-m", "initial commit"])
    except subprocess.CalledProcessError:
        # Some hooks auto-fix files on first attempt.
        run_command(["git", "add", "-A"])
        run_command(["git", "commit", "-m", "initial commit"])


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
    create_initial_commit()
    print("[cookiecutter] Bootstrap complete")


if __name__ == "__main__":
    main()
