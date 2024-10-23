from django.apps import apps
from pypdf import PdfReader
import docx
import re
from semantic_text_splitter import TextSplitter
from tokenizers import Tokenizer

from .llms import LLM
from .models import Chunk, User
from sentence_transformers import SentenceTransformer

class GenerateEmbeddings:
    chunks =[]
    text = ''
    embeddings = []
    llm = apps.get_app_config('rag').llm

    def __init__(self,chunks_or_text):
        if isinstance(chunks_or_text, list):
            self.chunks = chunks_or_text
        else:
            self.text = chunks_or_text
        self.generate_text_embeddings()
    
    def generate_text_embeddings(self):
        model = self.llm.get_embedding_model()
        # print(self.chunks)
        if len(self.chunks)>0:
            self.embeddings = model.encode(self.chunks)
        else:
            self.embeddings = model.encode(self.text).tolist()
        # print(self.embeddings)

class ChunkHandler:

    chunks =[]

    def __init__(self, text):
        self.split_into_chunks(text)

    def split_into_chunks(self,text):
        max_tokens = 100
        tokenizer = Tokenizer.from_pretrained("bert-base-cased")
        splitter = TextSplitter.from_huggingface_tokenizer(tokenizer, max_tokens,10)
        self.chunks = splitter.chunks(text)

class Extractor:
    cleaned_text = ''
    def __init__(self, id):
        document = User.objects.get(pk=id).document
        extracted_text = self.extract_text(document)
        self.cleaned_text = self.clean_text(extracted_text)
        # print(cleaned_text)
        
    
    def clean_text(self,text):
        txt = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('  ', ' ').replace("•", "").replace("*", "").replace("-", "").replace('  ','').replace(',',' ')
        punc_removed = re.sub(r'[:]', '', txt).lower()
        # print(punc_removed)
        return punc_removed
         
    def extract_text(self,document):
        if(document.name.split('.')[1] == 'pdf'):
            return self.extract_text_from_pdf(document)
        elif(document.name.split('.')[1] == 'docx'):
            return self.extract_text_from_doc(document)
        else:
            raise Exception("File type not supported")

    def extract_text_from_pdf(self,document):
        reader = PdfReader(document)
        text = "".join(page.extract_text() for page in reader.pages)
        # print(text)
        return text
    
    def extract_text_from_doc(self,doc):
        doc = docx.Document(doc)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        text = '\n'.join(fullText)
        return text

def get_document_instance_id(ns):
    temp =['uploads']
    temp.append(ns)
    print(ns)
    document_name = '/'.join(temp)
    print(document_name)
    id = User.objects.filter(document__icontains=document_name).first().id
    print(id)
    return id

def get_chunks(id):
    print(User.objects.get(id=id).chunks)
    return User.objects.get(id=id).chunks

def store_chunks(id,chunks):
    instance = Chunk.objects.get(id=id)
    instance.chunks = chunks
    instance.save()

def get_chunks_instance():
    inst = Chunk.objects.all().first()
    if inst is None:
        return create_chunk_instance()
    return inst.id


def create_chunk_instance():
    chunks = Chunk.objects.create(chunks=[])
    chunks.save()

    return chunks.id

