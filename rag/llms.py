
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
from django.conf import settings

class LLM:
    
    prompt_model_name = "deepset/roberta-base-squad2"
    embedding_model_name = "paraphrase-MiniLM-L6-v2"
    client = OpenAI(api_key=settings.OPENAI_KEY)

    def __init__(self):
        self.load_embedding_model()
        self.load_prompt_model()
    
    def load_prompt_model(self):
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.prompt_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.prompt_model_name)
    
    def load_embedding_model(self):
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

    def get_embedding_model(self):
        return self.embedding_model

    def process_prompt(self, prompt, context):
        inputs = self.tokenizer(prompt, context, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)


        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()

        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        res = self.tokenizer.decode(predict_answer_tokens)
        print(res)
        return res
    
    def openAI_model(self, question,context):
        prompt = f"""
        You will be provided with a question and some context. Your task is to generate an answer **only** based on the information provided in the context. Do not use any external knowledge or reasoning beyond what is explicitly stated in the context. If the context does not contain enough information to answer the question, respond with "I don't know."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        # Send the request to the OpenAI API
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",  # Specify "gpt-4" or "gpt-3.5-turbo" as per your use case
            prompt=prompt,
            max_tokens=150,  # Adjust as per your requirement
            temperature=0,   # Ensures deterministic output
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the model's answer from the response
        answer = response.choices[0].text.strip()
        print(answer)
        return answer

    