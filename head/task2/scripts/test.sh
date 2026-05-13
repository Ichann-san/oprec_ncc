#!/bin/bash
# =============================================
# LogPulse Mini SIEM — Test Script
# Runs the pytest test suite
# =============================================

set -e

echo "=========================================="
echo "  LogPulse Test Script"
echo "=========================================="

BACKEND_DIR="$(cd "$(dirname "$0")/../backend" && pwd)"

cd "${BACKEND_DIR}"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pytest pytest-asyncio httpx

# Run tests
echo ""
echo "🧪 Running tests..."
echo "------------------------------------------"

python -m pytest tests/ \
    -v \
    --tb=short \
    --junitxml=test-results.xml \
    2>&1

EXIT_CODE=$?

echo "------------------------------------------"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed! Exit code: ${EXIT_CODE}"
fi

echo "📄 Test report: ${BACKEND_DIR}/test-results.xml"
echo "=========================================="

exit $EXIT_CODE
