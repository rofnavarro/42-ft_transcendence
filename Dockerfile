FROM	python:3.10-bullseye

RUN		apt update && apt install -y postgresql-common postgresql-client

WORKDIR	/ft_transcendence

COPY	. .

RUN		pip install --upgrade pip
RUN		pip install --no-cache-dir -r ./requirements.txt

RUN		chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]