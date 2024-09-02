ALLPS		:= $(shell docker ps -a -q)
ALLIMG		:= $(shell docker images -a -q)
ALLVOL		:= $(shell docker volume ls -q)


HARDHAT		= hardhat

PWD_AUX		:= $(PWD)
# MARIA_P		= ./srcs/requirements/mariadb
# WPRESS_P	= ./srcs/requirements/wordpress
# NETWORK	= inception-network
all: images containers 
	${ALLPS}

images:
	docker build --tag ${HARDHAT}_image .

containers:
	docker run -d -p 8545:8545 ${HARDHAT}_image

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

fclean: stop rmall rmiall rmvall

re: fclean all
.PHONY: stop rmall rmiall rmvall