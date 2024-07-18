import os
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from chromadb import Client
import numpy as np

# Disable symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Initialize Chroma client with a persistence directory
client = Client(Settings(persist_directory="./chroma_db"))

# Load the Instructor model using SentenceTransformer
model = SentenceTransformer('hkunlp/instructor-base')

def generate_embedding(text, instruction="Represent the document:"):
    # Encode the text with the instruction to generate embeddings
    embeddings = model.encode([[instruction, text]])
    return embeddings[0]

# Create or get a Chroma collection
collection_name = 'document_embeddings'
collection = client.get_or_create_collection(collection_name)

# Example: Read extracted text from file with UTF-8 encoding
with open('extracted_text.txt', 'r', encoding='utf-8') as file:
    extracted_text = file.read()

# Generate embeddings for the extracted text
embedding = generate_embedding(extracted_text)

# Store the embeddings in Chroma
document_id = "unique_document_id_1"  # Replace with a meaningful ID
collection.add(
    documents=[extracted_text],
    embeddings=[embedding.tolist()],
    ids=[document_id]
)
print("Embedding stored successfully in Chroma with ID:", document_id)

def search_embeddings(query_text, instruction="Represent the query:"):
    # Generate embedding for query text
    query_embedding = generate_embedding(query_text, instruction)
    
    # Query Chroma collection for similar embeddings
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=5
    )
    return results

# Example query
query_text = "example query text"
results = search_embeddings(query_text)
for id, document, distance in zip(results['ids'][0], results['documents'][0], results['distances'][0]):
    print(f"Document ID: {id}")
    print(f"Content: {document}")
    print(f"Distance: {distance}")
    print("---")