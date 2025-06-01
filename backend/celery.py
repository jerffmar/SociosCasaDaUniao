
import os
from celery import Celery

# Defina o módulo de configurações padrão do Django para o 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Usar uma string aqui significa que o worker não precisa serializar
# o objeto de configuração para processos filhos.
# - namespace='CELERY' significa que todas as chaves de configuração do Celery
#   devem ter um prefixo `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega automaticamente tasks.py de todos os apps registrados no Django.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')