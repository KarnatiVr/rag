from django.apps import apps
from pypdf import PdfReader
import docx
import re
from semantic_text_splitter import TextSplitter
from tokenizers import Tokenizer

from .llms import LLM
from rag.models import User
from sentence_transformers import SentenceTransformer
import math

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

    def __init__(self, text, max_tokens, overlap):
        self.text = text
        self.max_tokens = max_tokens
        self.overlap = overlap
        # self.split_into_chunks(text)
        self.convert_txt_arr()
        self.fixed_size_chunk()

    def split_into_chunks(self,text):
        max_tokens = 50
        tokenizer = Tokenizer.from_pretrained("bert-base-cased")
        splitter = TextSplitter.from_huggingface_tokenizer(tokenizer, max_tokens,10)
        self.chunks = splitter.chunks(text)
    
    def convert_txt_arr(self):
        self.text = self.text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace(".", " ").replace("*", " ").replace("-", " ").replace(', ', ' ').replace('?',' ').replace('!', ' ')
        self.text = self.text.split(' ')
    
    def fixed_size_chunk(self):
        prev_chunk = ''
        curr_chunk = ''
        temp_chunks =[]
        text = self.text
        print("length of text is --->",len(text))
        while len(text) > 0:
            for word in text:
                if len(temp_chunks) < (self.max_tokens - self.overlap) and (len(temp_chunks) < len(text)):
                    print(temp_chunks)
                    temp_chunks.append(word)
                else:
                    curr_chunk = prev_chunk + ' '.join(temp_chunks)
                    # print(curr_chunk)
                    # print(temp_chunks)
                    self.chunks.append(curr_chunk)
                    index = self.max_tokens - self.overlap
                    prev_chunk = ' '.join(temp_chunks[index:])
                    break
            print(self.chunks)
            text = text[self.max_tokens-self.overlap:]
            temp_chunks=[]
        
        print(self.chunks)
                
                
        

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
    # print(ns)
    document_name = '/'.join(temp)
    # print(document_name)
    id = User.objects.filter(document__icontains=document_name).first().id
    # print(id)
    return id

def get_chunks(id):
    print(len(User.objects.get(id=id).chunks))
    
    return User.objects.get(id=id).chunks

def store_chunks(id,chunks):
    instance = User.objects.get(id=id)
    instance.chunks = chunks
    instance.save()
    
def zip_chunk_vector(embeddings, chunks):
    res = []
    for embbed, chunk in zip(embeddings.tolist(), chunks):
        res.append((embbed,chunk))
    return res


def retrieve_similar_vectors(vector_a, vector_set, top_k=0, threshold = 0.4):
    similar_chunks= []
    for i in range(len(vector_set)):
        similarity = cosine_similarity(vector_a, vector_set[i][0])
        print(similarity)
        if similarity > threshold:
            similar_chunks.append((similarity, vector_set[i][1]))

    # print(sorted(similar_chunks, key=lambda x: x[0], reverse=True)[:top_k])
    if top_k >0:
        similar_chunks = unzip_chunks(sorted(similar_chunks, key=lambda x: x[0], reverse=True)[:top_k])
        # print(similar_chunks)
        return similar_chunks
    return unzip_chunks(sorted(similar_chunks, key=lambda x: x[0], reverse=True))

def unzip_chunks(vector_set):
    chunks = []
    for i in range(len(vector_set)):
        chunks.append(vector_set[i][1])
    return chunks


def cosine_similarity(a,b):
  dot_p = 0
  for i in range(len(a)):
    dot_p = dot_p+a[i]*b[i]
  mag = find_magnitude(a)*find_magnitude(b)

  return dot_p/mag

def find_magnitude(a):
  mag = 0
  for i in a:
    mag = mag+i**2
  
  return math.sqrt(mag)
  


