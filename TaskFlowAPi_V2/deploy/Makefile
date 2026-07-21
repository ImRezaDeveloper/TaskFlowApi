.PHONY: up down logs ps

up:
	docker-compose -f deploy/docker-compose.yml up -d

down:
	docker-compose -f deploy/docker-compose.yml down

logs:
	docker-compose -f deploy/docker-compose.yml logs -f

ps:
	docker-compose -f deploy/docker-compose.yml ps

restart:
	docker-compose -f deploy/docker-compose.yml restart