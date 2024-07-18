#main.py
from embedder import Embedder
from vector_index import VectorIndex
from custom_retriever import CustomRetrieverWrapper
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def read_documents_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        documents = file.readlines()
    return [doc.strip() for doc in documents]

def setup_rag():
    # Step 1: Set up the embedding model
    embedder = Embedder()

    # Step 2: Read documents from a text file
    documents = read_documents_from_file('C:\\chatbot_project\\extracted_text.txt')
    embeddings = embedder.embed_text(documents)

    # Step 3: Initialize the vector index
    dimension = len(embeddings[0])
    vector_index = VectorIndex(dimension)
    vector_index.add_documents(embeddings, documents)

    # Step 4: Set up the Ollama LLM
    llm = Ollama(model="llama2")

    # Step 5: Create a custom prompt template
    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Step 6: Initialize the custom retriever
    retriever = CustomRetrieverWrapper(embedder=embedder, vector_index=vector_index)

    # Step 7: Create the RAG chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return rag_chain

def get_rag_chain():
    return setup_rag()

# Usage
if __name__ == "__main__":
    rag_chain = setup_rag()
    query = "What is the procedure for creating a VPC in AWS?"
    result = rag_chain.invoke({"query": query})
    print(result['result'])
