# AGENTS.md

## Project Overview

This repository runs a Snakemake pipeline that processes source inputs and produces output artifacts.

## Environment And Tooling

- Python: >=3.11 (managed via uv).
- Package install: uv sync
- Main pipeline entrypoint: snakemake --cores all

## Important Paths

- Raw inputs: data/raw/
- Outputs: outputs/
- Analysis scripts: scripts/analysis/
- Ingest scripts: scripts/ingest/

## Quality Gates

Configured checks are in .pre-commit-config.yaml:
- ruff (with --fix)
- ruff-format
- uv run ty check .
- pmd cpd --minimum-tokens 50 --language python -d scripts --exclude scripts/logs

Useful manual checks:
- uv run ruff check .
- uv run ruff format .
- uv run ty check .

## Common Commands

- Install dependencies: uv sync
- Run pipeline: snakemake --cores all
