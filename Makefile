ALLVOL            := $(shell docker volume ls -q)

all: up

up:
	sudo docker-compose --file=./docker-compose.yml --project-name=transcendence up --build -d

down:
	sudo docker-compose --file=./docker-compose.yml --project-name=transcendence down

cleanv:
	docker volume rm ${ALLVOL}

fclean: down cleanv
	docker system prune --all --force --volumes

re: fclean all

.PHONY: all up down flean re cleanv