.DEFAULT_GOAL := help

COMPOSE := docker compose

.PHONY: help up up-d down logs build build-api rebuild rebuild-d ps

help:
	@echo.
	@echo  Panaderia Zapatoca - Docker
	@echo  ===========================
	@echo.
	@echo   make up          Levanta API + PostgreSQL (build si hace falta)
	@echo   make up-d        Igual, en segundo plano
	@echo   make down        Detiene y elimina contenedores
	@echo   make rebuild     down + build --no-cache api + up  (tras cambios en Docker)
	@echo   make rebuild-d   rebuild en segundo plano
	@echo   make build-api   Solo reconstruye la imagen de la API sin cache
	@echo   make logs        Logs en vivo de todos los servicios
	@echo   make ps          Estado de contenedores
	@echo.

# Levantar stack completo
up:
	$(COMPOSE) up --build

up-d:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

build:
	$(COMPOSE) build

build-api:
	$(COMPOSE) build --no-cache api

# Reconstruccion limpia de la API y arranque (corrige entrypoint / Dockerfile)
rebuild: down build-api up

rebuild-d: down build-api
	$(COMPOSE) up --build -d
