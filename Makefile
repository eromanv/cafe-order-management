DOCKER_COMPOSE = sudo docker-compose

# Targets
.PHONY: help build up down logs migrate createsuperuser

build: ## Build the Docker containers
	$(DOCKER_COMPOSE) up --build -d

up: ## Start the Docker containers
	$(DOCKER_COMPOSE) up -d

down: ## Stop the Docker containers
	$(DOCKER_COMPOSE) down

logs: ## Show logs from the Docker containers
	$(DOCKER_COMPOSE) logs -f

migrate: ## Apply database migrations
	$(DOCKER_COMPOSE) exec web python manage.py migrate

createsuperuser: ## Create a superuser
	$(DOCKER_COMPOSE) exec web python manage.py createsuperuser