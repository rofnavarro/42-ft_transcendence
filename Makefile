ALLVOL            := $(shell docker volume ls -q)

all: up

up:
	sudo docker-compose --file=./docker-compose.yml --project-name=Transcendence up --build -d

down:
	sudo docker-compose --file=./docker-compose.yml --project-name=Transcendence down

cleanv:
	docker volume rm ${ALLVOL}
	sudo rm -rf /home/${LOGIN}

fclean: down cleanv
	docker system prune --all --force --volumes

re: fclean all

.PHONY: all up down flean re cleanv