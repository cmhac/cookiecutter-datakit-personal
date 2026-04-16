#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI is not installed in this devcontainer." >&2
  exit 1
fi

timeout_sec="${DOCKER_STARTUP_TIMEOUT_SEC:-30}"

echo "Waiting for Docker daemon to be ready (timeout: ${timeout_sec}s)..." >&2
for _ in $(seq 1 "${timeout_sec}"); do
  if docker info >/dev/null 2>&1 || sudo -n docker info >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
      exit 0
    fi
  fi
  sleep 1
done

echo "Docker is not available inside this devcontainer after ${timeout_sec}s." >&2
echo "Debug info:" >&2
echo "- docker version:" >&2
docker version >&2 || true
echo "- docker compose version:" >&2
docker compose version >&2 || true
exit 1
