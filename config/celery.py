import os
<<<<<<< HEAD

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
=======
from celery import Celery

# Establecer las configuraciones de Django por defecto para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('materiales_ecommerce')

# Usar las configuraciones en settings.py que inicien con el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir automáticamente tareas en los archivos tasks.py de cada aplicación instalada
>>>>>>> origin/feature/integracion-rag
app.autodiscover_tasks()
