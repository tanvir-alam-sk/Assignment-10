# scripts/pull_model.sh
#!/bin/bash

echo "Pulling Gemma model..."
docker-compose exec ollama ollama pull llama3.2:1b

echo "Model pulled successfully!"