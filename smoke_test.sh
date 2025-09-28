#!/bin/bash
set -e  # stop on first error

echo "🧹 Cleaning old data and logs..."
rm -rf data logs
mkdir -p data logs

echo "🚀 Building Docker image..."
docker-compose build

echo "🧪 Generating sample data..."
docker-compose run --rm pipeline python scripts/make_sample_data.py

echo "▶️ Running full pipeline..."
docker-compose run --rm pipeline

echo "📂 Checking outputs..."
ls -lh data/clean_data.csv data/agg_data.csv
tail -n 10 logs/pipeline.log || true

echo "🧪 Running tests..."
docker-compose run --rm pipeline pytest -v

echo "✅ Smoke test completed successfully!"
