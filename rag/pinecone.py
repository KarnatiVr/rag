from pinecone import  Pinecone
from pinecone import ServerlessSpec

class PineCone:
    pc = Pinecone(api_key="b7b4166f-5a03-438a-ab77-f74c02fb401b")
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
    
    def upsert_data(self, values):
        index = self.pc.Index("test-index")
        vectors =[]
        temp = 1
        for i in values:
            vectors.append({"id":str(temp) , "values": i})
            temp = temp+1
        # print("len of vectors",vectors)
        index.upsert(
        vectors=vectors,
        namespace="ns1"
        )

    def query(self, query_vector):
        index = self.pc.Index("test-index")
        # print(len(query_vector), query_vector)
        res = index.query(
            namespace="ns1",
            vector=query_vector,
            top_k=3,
            include_values=True
        )
        print(res)
        return res

    