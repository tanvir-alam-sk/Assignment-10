#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! PGPASSWORD=aa_nadim123 psql -h "postgresDB_Container" -U "aa_nadim" -d "scraping_db" -c '\q' 2>/dev/null; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done
echo "PostgreSQL is ready!"

echo "Waiting for Ollama..."
while ! curl -s "http://ollama:11434/api/tags" > /dev/null; do
    echo "Ollama is unavailable - sleeping"
    sleep 2
done
echo "Ollama is ready!"

echo "Running database migrations..."
python manage.py migrate

echo "Starting data generation sequence..."

# Set Python to unbuffered mode for real-time logging
export PYTHONUNBUFFERED=1

echo "Step 1: Rewriting property titles..."
python manage.py rewrite_titles --batch-size 2

echo "Step 2: Generating descriptions..."
python manage.py generate_descriptions --batch-size 2

echo "Step 3: Generating summaries..."
python manage.py generate_summaries --batch-size 2

echo "Step 4: Generating reviews..."
python manage.py generate_reviews --batch-size 2

echo "All data generation tasks completed!"

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000