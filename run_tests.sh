#!/bin/bash

# Test runner script for both services
set -e

echo "🧪 Running tests for both services..."

echo ""
echo "📋 Testing auth_service..."
cd auth_service
python -m pytest tests/ -v --cov=app --cov-report=term-missing
cd ..

echo ""
echo "📋 Testing todo_service..."
cd todo_service
python -m pytest tests/ -v --cov=app --cov-report=term-missing
cd ..

echo ""
echo "✅ All tests completed!"
