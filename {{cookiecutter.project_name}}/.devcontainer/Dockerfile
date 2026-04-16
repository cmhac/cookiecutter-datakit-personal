# Start from a Debian-based devcontainers base image (apt available).
FROM mcr.microsoft.com/devcontainers/base:debian-12

ARG PMD_VERSION="7.20.0"
ARG GO_VERSION="1.25.7"

ENV PATH="/usr/local/go/bin:/usr/local/bin:/opt/uv-python/current/bin:${PATH}"
ENV UV_PYTHON_INSTALL_DIR="/opt/uv-python"

USER root

# Install required packages via apt
RUN set -eux; \
  apt-get update; \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    findutils \
    git \
    openjdk-17-jre-headless \
    sudo \
    tar \
    unzip \
    ; \
  rm -rf /var/lib/apt/lists/*

# Install Go from official tarballs (newer than Debian repo).
RUN set -eux; \
  arch="$(uname -m)"; \
  case "${arch}" in \
    x86_64) go_arch="amd64" ;; \
    aarch64|arm64) go_arch="arm64" ;; \
    *) echo "Unsupported architecture for Go: ${arch}" >&2; exit 1 ;; \
  esac; \
  curl -fsSLo /tmp/go.tgz "https://go.dev/dl/go${GO_VERSION}.linux-${go_arch}.tar.gz"; \
  rm -rf /usr/local/go; \
  tar -C /usr/local -xzf /tmp/go.tgz; \
  rm /tmp/go.tgz; \
  /usr/local/go/bin/go version

# Install uv (https://docs.astral.sh/uv/) and ensure Python 3.12 is available.
RUN set -eux; \
  curl -LsSf https://astral.sh/uv/install.sh | sh; \
  install -m 0755 /root/.local/bin/uv /usr/local/bin/uv; \
  rm -rf /root/.local; \
  uv python install 3.12 --install-dir "${UV_PYTHON_INSTALL_DIR}"; \
  python_bin="$(find "${UV_PYTHON_INSTALL_DIR}" -type f -path '*/bin/python3.12' | head -n 1)"; \
  test -n "${python_bin}"; \
  python_home="$(dirname "$(dirname "${python_bin}")")"; \
  ln -sfn "${python_home}" /opt/uv-python/current; \
  ln -sf /opt/uv-python/current/bin/python3.12 /usr/local/bin/python3.12; \
  ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3; \
  ln -sf /usr/local/bin/python3.12 /usr/local/bin/python

# Install AWS CLI v2 (needed by outputs_pull.sh).
RUN set -eux; \
  arch="$(uname -m)"; \
  case "${arch}" in \
    x86_64) aws_arch="x86_64" ;; \
    aarch64|arm64) aws_arch="aarch64" ;; \
    *) echo "Unsupported architecture for AWS CLI: ${arch}" >&2; exit 1 ;; \
  esac; \
  curl -sSLo /tmp/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-${aws_arch}.zip"; \
  unzip -q /tmp/awscliv2.zip -d /tmp; \
  /tmp/aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update; \
  rm -rf /tmp/aws /tmp/awscliv2.zip

# Install PMD for the repo's pre-commit "cpd" hook.
RUN set -eux; \
  curl -sSLo /tmp/pmd.zip "https://github.com/pmd/pmd/releases/download/pmd_releases%2F${PMD_VERSION}/pmd-dist-${PMD_VERSION}-bin.zip"; \
  unzip -q /tmp/pmd.zip -d /opt; \
  ln -sf "/opt/pmd-bin-${PMD_VERSION}/bin/pmd" /usr/local/bin/pmd; \
  rm /tmp/pmd.zip

# `remoteUser`/`USER` do not create accounts; `devpod-user` must exist in /etc/passwd.
RUN set -eux; \
  if ! id -u devpod-user >/dev/null 2>&1; then \
    existing_user="$(getent passwd 1000 | cut -d: -f1 || true)"; \
    if [ -n "${existing_user}" ]; then \
      if [ "${existing_user}" != "devpod-user" ]; then usermod -l devpod-user "${existing_user}"; fi; \
      existing_group="$(getent group 1000 | cut -d: -f1 || true)"; \
      if [ -n "${existing_group}" ] && [ "${existing_group}" != "devpod-user" ]; then groupmod -n devpod-user "${existing_group}" || true; fi; \
      usermod -d /home/devpod-user -m devpod-user; \
    else \
      if ! getent group 1000 >/dev/null 2>&1; then groupadd --gid 1000 devpod-user; fi; \
      useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash devpod-user; \
    fi; \
  fi; \
  usermod -aG sudo devpod-user; \
  if ! getent group docker >/dev/null 2>&1; then groupadd --system docker; fi; \
  usermod -aG docker devpod-user; \
  echo "devpod-user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/devpod-user; \
  chmod 0440 /etc/sudoers.d/devpod-user; \
  chown -R devpod-user:devpod-user "${UV_PYTHON_INSTALL_DIR}"; \
  chmod -R g+w "${UV_PYTHON_INSTALL_DIR}"

# install subfinder with go
RUN set -eux; \
  GOBIN=/usr/local/bin go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

USER devpod-user
