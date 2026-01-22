.PHONY: help build up down restart logs migrate createsuperuser shell test clean

help:
	@echo "School Management System - Docker Commands"
	@echo "=========================================="
	@echo "build          - Build Docker images"
	@echo "up             - Start all services"
	@echo "down           - Stop all services"
	@echo "restart        - Restart all services"
	@echo "logs           - View logs"
	@echo "migrate        - Run database migrations"
	@echo "createsuperuser- Create Django superuser"
	@echo "shell          - Open Django shell"
	@echo "test           - Run tests"
	@echo "clean          - Remove containers and volumes"
	@echo "dev            - Start in development mode"
	@echo "prod           - Start in production mode"

build:
	docker compose build

up:
	docker compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@docker compose exec backend python manage.py migrate
	@echo "Services are up! Access at http://localhost:8000"

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

migrate:
	docker compose exec backend python manage.py makemigrations
	docker compose exec backend python manage.py migrate

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

shell:
	docker compose exec backend python manage.py shell

dbshell:
	docker compose exec db mysql -u ${DB_USER} -p${DB_PASSWORD} ${DB_NAME}

test:
	docker compose exec backend python manage.py test

clean:
	docker compose down -v
	docker system prune -f

dev:
	@export ENVIRONMENT=development && docker compose up -d
	@echo "Development environment started"

prod:
	@export ENVIRONMENT=production && docker compose up -d
	@echo "Production environment started"

backup-db:
	docker compose exec db mysqldump -u ${DB_USER} -p${DB_PASSWORD} ${DB_NAME} > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	@read -p "Enter backup file path: " file; \
	docker compose exec -T db mysql -u ${DB_USER} -p${DB_PASSWORD} ${DB_NAME} < $$file