# Hotel Content Generator with Ollama

This project is a Django CLI application designed to re-write property information using the Ollama model. The application fetches property details, rewrites the titles and descriptions, generates a summary, and creates ratings and reviews using an LLM model. All data is stored in a PostgreSQL database using Django ORM.

## Prerequisites

- Docker and Docker Compose
- Git
- Python 3.11 or higher (for local development)
- PostgreSQL database with hotel data

## Environment Setup

### Clone the repository

```bash
git clone https://github.com/tanvir-alam-sk/Assignment-10 ollama-property-rewriter
cd ollama-property-rewriter
```

For this project we need to run assignment 8.

[https://github.com/tanvir-alam-sk/assignment-8-raf]([https://github.com/tanvir-alam-sk/assignment-8-raf])

### **Create a virtual environment and activate it:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### **Install dependencies:**

```bash
pip install -r requirements.txt
  
```

### Build and start the containers:

```
docker-compose up -d --build
```

### Running the Application

```bash
docker-compose up --build
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

## Run Test

```
python manage.py test
coverage report
```

## Monitoring and Maintenance

### View Logs

1. View Django app logs:
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

### Error Logs

1. Check the logs if you encounter issues:
   ```bash
   docker-compose logs --tail=100 ollama    # Last 100 lines of Ollama logs
   docker-compose logs --tail=100 django_app # Last 100 lines of Django logs
   ```

```

```
