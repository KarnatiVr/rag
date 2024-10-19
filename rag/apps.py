from django.apps import AppConfig
from .pinecone import PineCone

class RagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rag'
    pineCone = PineCone()

    def ready(self):
        self.pineCone.__int__()
  
