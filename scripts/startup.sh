# scripts/startup.sh
#!/bin/bash

# Stop any existing containers
docker-compose down

# Remove existing volumes (optional - uncomment if needed)
# docker-compose down -v

# Start services
docker-compose up -d --build

# Wait for services to be healthy
echo "Waiting for services to become healthy..."
sleep 30

# Check if services are running
docker-compose ps

# Pull the Gemma model
echo "Pulling Gemma model..."
docker-compose exec -T ollama ollama pull llama3.2:1b

echo "Setup completed!"