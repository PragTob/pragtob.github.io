FROM ruby:3.3-bookworm

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash vscode

WORKDIR /workspaces

RUN gem install bundler

USER vscode