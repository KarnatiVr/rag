
from django.apps import apps

from .models import Chat, User
from .utils import ChunkHandler, Extractor, GenerateEmbeddings, get_chunks, get_chunks_instance, get_document_instance_id, store_chunks


class RagPipeline:

    

    def __init__(self):
        # self.document_instance_id = id
        # self.extract_and_chunk()
        print("pipeline initialised")
        self.set_initial_state()
        self.chunk_instance_id = get_chunks_instance()

    def set_initial_state(self):
        self.pineCone = apps.get_app_config('rag').pineCone
        self.llm = apps.get_app_config('rag').llm
        self.document_instance_id = 0
        self.cleaned_text = ''
        self.chunks = []
        self.embeddings = []
        self.query_vector = []
        self.query_matches = []
        self.query_result = []
        self.question = ''
        self.context = ''
        self.answer = ''
        self.doc_choice=''

    def process_doc(self,id):
        self.document_instance_id = id
        self.current_doc_md=User.objects.get(id=id).document.name.split('/')[1]
        
        self.extract_and_chunk()

    def extract_and_chunk(self):
        extractor = Extractor(self.document_instance_id)
        self.cleaned_text = extractor.cleaned_text
        # self.chunks = ChunkHandler(self.cleaned_text).chunks
        chunks = ChunkHandler(self.cleaned_text).chunks
        self.chunks.extend(chunks)
        store_chunks(self.chunk_instance_id,self.chunks)
        print("chunks")
        print(len(self.chunks))
        self.embedd_text(chunks)

    def embedd_text(self, chunks):
        self.embeddings = GenerateEmbeddings(chunks).embeddings
        print("embeddings")
        print(len(self.embeddings))
        self.store_embeddings()

    def store_embeddings(self):
        self.pineCone.upsert_data(self.embeddings,self.current_doc_md)
        # self.chunks = []
        # self.convert_query_to_vector("what is performance testing?")

    def convert_query_to_vector(self, id, ns=None):
        self.question = Chat.objects.get(id=id).input
        self.doc_choice = Chat.objects.get(id=id).choice.split('/')[1]
        # self.document_instance_id = get_document_instance_id(ns)
        self.query_vector = GenerateEmbeddings(self.question).embeddings
        self.current_doc_md = self.doc_choice
        return self.query_pinecone()
    
    def query_pinecone(self):
        self.query_results = self.pineCone.query(self.query_vector, self.current_doc_md)
        return self.post_process()

    def post_process(self):
        # print(self.query_results)
        self.chunks = get_chunks(self.chunk_instance_id)
        print(len(self.chunks))
        if len(self.query_results) > 0:
            for item in self.query_results:
                txt = self.chunks[int(item['id'])-1]
                self.query_matches.append(txt)
                self.context = self.context+txt
        return self.generate_answer()
            # print(txt)
            # print(len(self.chunks), len(self.embeddings))
    
    def generate_answer(self):
        print("question----->",self.question)
        print("context----->",self.context)
        # self.answer = self.llm.process_prompt(self.question, self.context)
        self.answer = self.llm.openAI_model(self.question, self.context)
        return self.answer

    def delete_data(self):
        self.set_initial_state()

        
    