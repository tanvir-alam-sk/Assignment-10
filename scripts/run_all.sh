# scripts/run_all.sh
#!/bin/bash

# First, make sure containers are up
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Pull the model
./scripts/pull_model.sh

# Run the commands
echo "Running all commands..."

commands=("rewrite_titles" "generate_descriptions" "generate_summaries" "generate_reviews")

for cmd in "${commands[@]}"; do
    echo "Running $cmd..."
    docker-compose exec -T django_app python manage.py $cmd --batch-size 2
    echo "$cmd completed"
    sleep 5
done

echo "All commands completed!"