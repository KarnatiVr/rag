
from django.apps import apps
from .utils import ChunkHandler, Extractor, GenerateEmbeddings


class RagPipeline:
    pineCone = apps.get_app_config('rag').pineCone
    document_instance_id = 0
    cleaned_text = ''
    chunks = []
    embeddings = []
    query_vector = []

    def __init__(self, id):
        self.document_instance_id = id
        self.extract_and_chunk()

    def extract_and_chunk(self):
        extractor = Extractor(self.document_instance_id)
        self.cleaned_text = extractor.cleaned_text
        self.chunks = ChunkHandler(self.cleaned_text).chunks
        self.embedd_text()

    def embedd_text(self):
        self.embeddings = GenerateEmbeddings(self.chunks).embeddings
        self.store_embeddings()

    def store_embeddings(self):
        self.pineCone.upsert_data(self.embeddings)
        self.convert_query_to_vector("what is unit testing?")

    def convert_query_to_vector(self, query):
        self.query_vector = GenerateEmbeddings(query).embeddings
        
        self.query_pinecone()
    
    def query_pinecone(self):
        self.pineCone.query(self.query_vector)

    def post_process(self):
        pass
    