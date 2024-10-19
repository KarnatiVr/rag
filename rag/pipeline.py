
from .utils import ChunkHandler, Extractor, GenerateEmbeddings


class RagPipeline:

    document_instance_id = 0
    cleaned_text = ''
    chunks = ''

    def __init__(self, id):
        self.document_instance_id = id
        self.extract_and_chunk()

    def extract_and_chunk(self):
        extractor = Extractor(self.document_instance_id)
        self.cleaned_text = extractor.cleaned_text
        self.chunks = ChunkHandler(self.cleaned_text).chunks
        self.embedd_text()

    def embedd_text(self):
        GenerateEmbeddings(self.cleaned_text)
        


    def store_embeddings():
        pass
        
    