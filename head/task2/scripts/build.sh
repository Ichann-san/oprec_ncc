#!/bin/bash
# =============================================
# LogPulse Mini SIEM — Build Script
# Builds the Docker image for the backend
# =============================================

set -e

echo "=========================================="
echo "  LogPulse Build Script"
echo "=========================================="

# Configuration
IMAGE_NAME="${DOCKER_IMAGE:-logpulse-backend}"
IMAGE_TAG="${DOCKER_TAG:-latest}"
BACKEND_DIR="$(cd "$(dirname "$0")/../backend" && pwd)"

echo "📦 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "📁 Build context: ${BACKEND_DIR}"

# Navigate to backend directory
cd "${BACKEND_DIR}"

# Build the Docker image
docker build \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    -t "${IMAGE_NAME}:latest" \
    --no-cache \
    .

echo ""
echo "✅ Build complete!"
echo "   Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "   Image: ${IMAGE_NAME}:latest"

# Show image info
docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

echo "=========================================="
