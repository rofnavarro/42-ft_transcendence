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
gunicorn --bind 0.0.0.0:8000 ft_transcendence.wsgi

python3 manage.py shell -c "\
from users.models import CustomUser;\
user = CustomUser(username='$SUPER_USER', email='$SUPER_MAIL', is_staff=True, is_superuser=True);\
user.save();\
user.set_password('$SUPER_PASSWORD');\
user.save();\
exit();"


# Inicializa o servidor do Django
echo	"Starting Django server..."
exec	python manage.py runserver_plus --cert-file ./localhost.crt --key-file ./localhost.key 0.0.0.0:8000
