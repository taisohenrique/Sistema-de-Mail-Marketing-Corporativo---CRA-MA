import os
from celery import Celery

# Diz ao Celery para usar as configurações do nosso Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Puxa as configurações do settings.py que começam com "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Procura automaticamente por arquivos chamados "tasks.py" nos nossos módulos
app.autodiscover_tasks()