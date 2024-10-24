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
            self.upsert_data(values)
    
    def upsert_data(self, values, md):
        index = self.pc.Index("test-index")
        self.last_index = self.get_length_index()
        vectors =[]
        temp = 0
        for i in values:
            vectors.append({"id":str(self.last_index) , "values": i,"metadata": {"doc_name":md}})
            self.last_index = self.last_index+1
        # print("len of vectors",vectors)
        index.upsert(
        vectors=vectors,
        namespace=self.namespace,
        
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

    def query(self, query_vector, md=None):
        index = self.pc.Index("test-index")
        print(md)
        # print(len(query_vector), query_vector)
        if md is not None:
            res = index.query(
                namespace=self.namespace,
                vector=query_vector,
                top_k=5,
                include_values=True,
                filter={"doc_name":{"$eq": md}},
                include_metadata=True
            )
        else :
            res = index.query(
                namespace=self.namespace,
                vector=query_vector,
                top_k=5,
                include_values=True
            )
        # print(res)
        # with open("output.txt", "w") as f:
        #     f.write(str(res))
        # print(res)
        return res['matches']
    

    def get_length_index(self):
        index = self.pc.Index("test-index")
        last_id = 0
        for i in index.list(namespace=self.namespace):
            last_id = last_id+len(i)

        return last_id
        

    