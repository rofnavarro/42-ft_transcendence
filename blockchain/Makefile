ALLPS		:= $(shell docker ps -a -q)
ALLIMG		:= $(shell docker images -a -q)
ALLVOL		:= $(shell docker volume ls -q)


HARDHAT		= hardhat

# NETWORK = transcendence-network

PWD_AUX		:= $(shell $PWD)
# MARIA_P		= ./srcs/requirements/mariadb
# WPRESS_P	= ./srcs/requirements/wordpress
# NETWORK	= inception-network
all: volumes images containers 
	${ALLPS}

# network:
# 	docker network create ${NETWORK}

#TODO: precisamos conseguir compartilhar com precisao a pasta artifacts
volumes:
	mkdir -p ./${HARDHAT}/artifacts
	docker volume create --opt o=bind --opt type=none --opt device=${PWD_AUX}/${HARDHAT}/artifacts ${HARDHAT}-volume

images:
	docker build --tag ${HARDHAT}_image .

containers:
	docker run -d -p 8545:8545 -v ${PWD_AUX}/hardhat/artifacts:/app/hardhat/artifacts/ ${HARDHAT}_image
stop:
	docker stop ${ALLPS}

start:
	docker start ${ALLPS}

rmall:
	docker rm ${ALLPS}

rmiall:
	docker rmi ${ALLIMG}

rmvall:
	docker volume rm ${ALLVOL}

fclean: stop rmall rmvall rmiall

re: fclean all
.PHONY: stop rmall rmiall rmvall