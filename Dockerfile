FROM	python:3.10-bullseye

RUN		apt update && apt install -y postgresql-common postgresql-client openssl

WORKDIR	/ft_transcendence

COPY	. .

RUN		openssl req -batch -x509 -sha256 -nodes -newkey rsa:2048 -days 365 \
		-keyout ./localhost.key \
		-out ./localhost.crt

RUN		pip install --upgrade pip
RUN		pip install --no-cache-dir -r ./requirements.txt

RUN		chmod +x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]