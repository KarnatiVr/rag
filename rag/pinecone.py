from pinecone import  Pinecone
from pinecone import ServerlessSpec
from django.conf import settings

class PineCone:
    pc = Pinecone(api_key=settings.PINECONE_KEY)
    index_name = "test-index"
    namespace = "test-namespace"
    last_index = 0
    
    def __int__(self):
        print("Pinecone initialized")
        if not self.pc.has_index(self.index_name):
            self.create_index()

    def create_index(self):
        self.pc.create_index(
        name=self.index_name,
        dimension=384,
        metric="cosine",
        timeout=50,
        spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    def upsert_or_update(self, values):
        self.last_index = self.get_length_index()
        if self.last_index == 0:
            self.upsert_data(values)
        else:
            self.update_data(values)
    
    def upsert_data(self, values):
        index = self.pc.Index("test-index")
        vectors =[]
        temp = 0
        for i in values:
            vectors.append({"id":str(temp) , "values": i})
            temp = temp+1
        # print("len of vectors",vectors)
        self.last_index = temp
        index.upsert(
        vectors=vectors,
        namespace=self.namespace
        )

    def update_data(self, values):
        index= self.pc.Index("test-index")
        vectors =[]
        for i in values:
            vectors.append({"id":str(self.last_index), "values": i})
            self.last_index = self.last_index+1
        index.update(
            vectors=vectors,
            namespace=self.namespace
        )

    


    def query(self, query_vector,ns):
        index = self.pc.Index("test-index")
        # print(len(query_vector), query_vector)
        res = index.query(
            namespace=ns,
            vector=query_vector,
            top_k=5,
            include_values=True
        )
        # print(res)
        # with open("output.txt", "w") as f:
        #     f.write(str(res))
        return res['matches']
    

    def get_length_index(self):
        index = self.pc.Index("test-index")
        return len(index.list(namespace=self.namespace))
        

    