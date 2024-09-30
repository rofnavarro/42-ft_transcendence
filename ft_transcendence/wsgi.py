import os
import atexit
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')
django.setup()

def	set_all_users_offline():
	from users.models import CustomUser
	CustomUser.objects.filter(is_online=True).update(is_online=False)

atexit.register(set_all_users_offline)

application = get_wsgi_application()
