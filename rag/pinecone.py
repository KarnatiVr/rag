from pinecone import  Pinecone
from pinecone import ServerlessSpec
from django.conf import settings

class PineCone:
    pc = Pinecone(api_key=settings.PINECONE_KEY)
    index_name = "test-index"
    
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
    
    def upsert_data(self, values, namespace):
        index = self.pc.Index("test-index")
        vectors =[]
        temp = 1
        for i in values:
            vectors.append({"id":str(temp) , "values": i})
            temp = temp+1
        # print("len of vectors",vectors)
        index.upsert(
        vectors=vectors,
        namespace=namespace
        )
    


    def query(self, query_vector,ns):
        index = self.pc.Index("test-index")
        # print(len(query_vector), query_vector)
        res = index.query(
            namespace=ns,
            vector=query_vector,
            top_k=7,
            include_values=True
        )
        # print(res)
        # with open("output.txt", "w") as f:
        #     f.write(str(res))
        return res['matches']

    