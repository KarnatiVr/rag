from pypdf import PdfReader
import docx
import re
from semantic_text_splitter import TextSplitter
from transformers import BertTokenizer

from rag.models import User
from sentence_transformers import SentenceTransformer


class GenerateEmbeddings:
    text = ''
    def __init__(self,text):
        self.text = text
        self.generate_text_embeddings(self.text)
    
    def generate_text_embeddings(self, text):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Sentences we want to encode. Example:
        sentence = ['This framework generates embeddings for each input sentence']

        # Sentences are encoded by calling model.encode()
        embedding = model.encode(sentence)

class ChunkHandler:

    chunks =''

    def __init__(self, text):
        self.split_into_chunks(text)

    def split_into_chunks(self,text):
        max_tokens = 1000
        # tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
        # splitter = TextSplitter.from_huggingface_tokenizer(tokenizer, max_tokens)
        splitter = TextSplitter((200,1000))
        self.chunks = splitter.chunks(text)
        print(self.chunks)
        

class Extractor:
    cleaned_text = ''
    def __init__(self, id):
        document = User.objects.get(pk=id).document
        extracted_text = self.extract_text(document)
        self.cleaned_text = self.clean_text(extracted_text)
        # print(cleaned_text)
        
    
    def clean_text(self,text):
        txt = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('  ', ' ').replace("•", "").replace("*", "").replace("-", "").replace('  ','')
        punc_removed = re.sub(r'[:]', '', txt).lower()
        print(punc_removed)
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
  