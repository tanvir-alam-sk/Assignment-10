## Ollama using Docker.Compose

```/binsh

version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ./ollama:/root/.ollama
    restart: unless-stopped
    command: serve

```

- Create a `docker-compose.yml` file with above content 
- docker-compose up -d 
- Access olama on the exposed port.


> To load Model using olama docker 
- get inside Ollama docker
    - docker exec -it ollama /bin/bash 
- pull and load a model
    - ollama pull mistral:instruct
    - ollama pull llama3                 

- lists all available model
    - ollama list                  
- remove a model
    - ollama rm llama3   

- You can use any other method to load load a model.              
