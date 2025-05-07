.PHONY: build up down logs test

build:
	docker build -t fastapi-app .

up:
	docker run --rm -it -p 8088:8088 fastapi-app

down:
	@echo "Use Ctrl+C to stop the running container."

logs:
	docker logs fastapi-app

test:
	pytest