# Hotel Content Generator with Ollama

This Django application uses Ollama to generate enhanced content for hotel listings, including descriptions, reviews, and summaries.

## Prerequisites
- Docker and Docker Compose
- Git
- Python 3.11 or higher (for local development)
- PostgreSQL database with hotel data

## Environment Setup
1. Clone the repository
    ```bash
    git clone <repository-url>
    cd ollama-prop-rewriter
    ```

2. Create a .env file in the root directory:
    ```bash
    DB_USERNAME=aa_nadim
    DB_PASSWORD=aa_nadim123
    DB_NAME=scraping_db
    DB_PORT=5432
    DB_HOST=postgres
    OLLAMA_BASE_URL=http://ollama:11434/api/generate
    SECRET_KEY='django-insecure-nc4($e*vaa^7ftbpg^5y8yz-5a(-n18-*#ln^wpbtw5a0-@e5('
    ```

## Running the Application

### Starting the Services

```bash
docker-compose up --build ollama
docker-compose ps
docker-compose up --build django_app
docker-compose ps

docker-compose exec ollama bash 
ollama list 
ollama rm gemma2:2b                                            
docker-compose exec ollama ollama pull llama3.2:1b 

docker-compose exec django_app python manage.py rewrite_titles --batch-size 1
docker-compose exec django_app python manage.py generate_descriptions --batch-size 1
docker-compose exec django_app python manage.py generate_summaries --batch-size 1
docker-compose exec django_app python manage.py generate_reviews --batch-size 1


chmod +x scripts/startup.sh
./scripts/startup.sh
./scripts/run_all.sh
```

1. Build and start the containers:
    ```
    docker-compose up -d --build
    ```
   Wait for the services to be ready (about 30 seconds)

2. Verify the services are running:
   ```
   docker-compose ps
   ```

### Running Content Generation Commands

Each command below processes hotels in batches. You can adjust the batch size using the --batch-size parameter.

1. Rewrite hotel titles:
   ```
   docker-compose exec django_app python manage.py rewrite_titles --batch-size 2
   ```
2. Generate hotel descriptions:
   ```
   docker-compose exec django_app python manage.py generate_descriptions --batch-size 2
   ```
3. Generate hotel summaries:
   ```
   docker-compose exec django_app python manage.py generate_summaries --batch-size 2
   ```
4. Generate hotel reviews:
   ```
   docker-compose exec django_app python manage.py generate_reviews --batch-size 2
   ```
### Running All Commands at Once

```
./scripts/run_all.sh
```

## Monitoring and Maintenance

### View Logs

1. View Ollama service logs:
   ```
   docker-compose logs ollama
   ```
2. View Django app logs:
   ```
   docker-compose logs django_app
   ```

## Database Management

Access the Django admin interface:

1. Create a superuser:
   ```
   docker-compose exec django_app python manage.py createsuperuser
   ```

Visit http://localhost:8000/admin and log in with your superuser credentials

## Troubleshooting

### Common Issues

1. Ollama Service Not Starting
- Ensure ports are not in use
- Check system resources
- Review Ollama logs

2. Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in .env
- Ensure database exists and is accessible

3. Timeout Errors
- Increase timeout value in OllamaService class
- Reduce batch size
- Check system resources

### Error Logs

1. Check the logs if you encounter issues:
   ```bash
   docker-compose logs --tail=100 ollama    # Last 100 lines of Ollama logs
   docker-compose logs --tail=100 django_app # Last 100 lines of Django logs
  ```