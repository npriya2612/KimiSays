#embedder
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name='hkunlp/instructor-base'):
        print("Initializing Embedder with model:", model_name)
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, texts, instruction="Represent the text:"):
        print(f"Embedding texts: {texts}")
        embeddings = self.model.encode([f"{instruction} {text}" for text in texts])
        # Convert numpy arrays to lists
        embeddings_list = [embedding.tolist() for embedding in embeddings]
        print(f"Generated embeddings: {embeddings_list}")
        return embeddings_list
