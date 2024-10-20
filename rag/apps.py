from django.apps import AppConfig

from .llms import LLM
from .pinecone import PineCone

class RagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rag'
    pineCone = PineCone()
    llm = LLM()

    # def ready(self):
        # self.pineCone.__int__()
        # self.llm.__init__()
  
