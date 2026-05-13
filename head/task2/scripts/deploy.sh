#!/bin/bash
# =============================================
# LogPulse Mini SIEM — Deploy Script
# Deploys the full stack using Docker Compose
# =============================================

set -e

echo "=========================================="
echo "  LogPulse Deploy Script"
echo "=========================================="

BACKEND_DIR="$(cd "$(dirname "$0")/../backend" && pwd)"
HEALTH_URL="http://localhost:8000/health"
MAX_RETRIES=10
RETRY_INTERVAL=3

cd "${BACKEND_DIR}"

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose down 2>/dev/null || true

# Start all services
echo "🚀 Starting all services..."
docker compose up -d --build

# Wait for services to start
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Health check with retries
echo "💓 Running health check..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -sf "${HEALTH_URL}" > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    fi

    if [ $i -eq $MAX_RETRIES ]; then
        echo "❌ Health check failed after ${MAX_RETRIES} attempts!"
        echo "   Check logs: docker compose logs backend"
        exit 1
    fi

    echo "   Attempt ${i}/${MAX_RETRIES} — waiting ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

# Show running containers
echo ""
echo "📦 Running containers:"
docker compose ps

echo ""
echo "=========================================="
echo "  🎉 Deployment successful!"
echo "=========================================="
echo ""
echo "  Services:"
echo "    Backend:    http://localhost:8000"
echo "    Prometheus: http://localhost:9090"
echo "    Grafana:    http://localhost:3000"
echo "    SonarQube:  http://localhost:9000"
echo "    Jenkins:    http://localhost:8080"
echo ""
echo "=========================================="
