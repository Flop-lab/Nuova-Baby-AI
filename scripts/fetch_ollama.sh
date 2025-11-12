#!/bin/bash
set -e

OLLAMA_VERSION="0.12.10"
BINARIES_DIR="src-tauri/binaries"

# SHA256 checksum (VERIFIED from official release)
OLLAMA_SHA256="cd05049d4202091629403a33a5f345a584fcd86cd82e66c1fbe9c23c5f39f175"

echo "📦 Downloading Ollama Server v${OLLAMA_VERSION}..."

mkdir -p "$BINARIES_DIR"
cd "$BINARIES_DIR"

# Download universal binary (works on both Apple Silicon and Intel)
if [ ! -f "ollama" ]; then
    echo "⬇️  Downloading universal binary..."
    curl -L -o ollama-darwin.tgz \
        "https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}/ollama-darwin.tgz"

    # Extract binary
    tar -xzf ollama-darwin.tgz ollama
    rm ollama-darwin.tgz

    # Verify checksum
    echo "${OLLAMA_SHA256}  ollama" | shasum -a 256 -c -

    chmod 755 ollama
    echo "✅ Universal binary ready ($(du -h ollama | cut -f1))"
else
    echo "✅ Ollama binary already exists"
fi

echo "🎉 Ollama binary ready!"
