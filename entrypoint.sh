#!/bin/bash

# Aguarda o serviço do PostgreSQL estar disponível
echo	"Waiting for PostgreSQL to be ready..."
until	PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c '\q'; do
  >&2 echo	"Postgres is unavailable - sleeping"
  sleep	2
done

# Aplica as migrações do Django
echo	"Applying database migrations..."
python	manage.py makemigrations
python	manage.py migrate


# Inicializa o servidor do Django
echo	"Starting Django server..."
exec	python manage.py runserver 0.0.0.0:8000