FROM mcr.microsoft.com/devcontainers/miniconda:1-3

ARG PIXI_VERSION=v0.40.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget curl git procps zsh build-essential python3-dev \
    # To remove the image size, it is recommended refresh the package cache as follows
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -o /usr/local/bin/pixi -fsSL --compressed "https://github.com/prefix-dev/pixi/releases/download/${PIXI_VERSION}/pixi-$(uname -m)-unknown-linux-musl" \
    && chmod +x /usr/local/bin/pixi \
    && pixi info

# Instal zsh with git plugin and default theme
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.1/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git