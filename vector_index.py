import faiss
import numpy as np

class VectorIndex:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
    
    def add_documents(self, embeddings, documents):
        if len(embeddings) != len(documents):
            raise ValueError("The number of embeddings must match the number of documents")
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(documents)
    
    def search(self, query_embedding, top_k=5):
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [(self.documents[i], distances[0][i]) for i in indices[0]]
