
# KimiSays - Customized LLM Chatbot

KimiSays is a customized LLM (Large Language Model) chatbot built using Streamlit and LangChain libraries to facilitate interactive query handling and document retrieval.

## Features

- **Custom LLM Chatbot Interface**: Provides an intuitive UI powered by Streamlit for users to interact with the chatbot.
- **Document Retrieval**: Uses a custom retriever to fetch relevant documents based on user queries.
- **Integration with Sentence Embeddings**: Utilizes SentenceTransformer for embedding text and faiss for efficient similarity search.

## Components

### Files and Modules

- **app.py**: Main Streamlit application setup for the chatbot interface and interaction.
- **rag.py**: Configures the RAG (Retrieval-Augmented Generation) chain using LangChain for document retrieval and answering user queries.
- **custom_retriever.py**: Defines a custom retriever class for fetching relevant documents based on embeddings.
- **embedder.py**: Initializes the SentenceTransformer model for text embedding.
- **test_url.py**: Streamlit app to authenticate with Google Drive API and extract text from various file formats like PDF, DOCX, and URLs.
- **util.py**: Contains utility functions for text extraction from PDFs, DOCX files, URLs, and text cleaning.
- **vector_index.py**: Implements a VectorIndex class using faiss for efficient document search based on embeddings.

### Installation and Setup

1. **Clone Repository**: `git clone https://github.com/npriya2612/kimisays.git`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Run Streamlit App**: `streamlit run app.py`

### Usage

- Start the Streamlit app by running `streamlit run app.py`.
- Enter your query in the provided text input to interact with the chatbot.
- View the search results and relevant documents fetched by the chatbot.

### Example

```python
# Example usage
rag_chain = setup_rag()
query = "What is the procedure for creating a VPC in AWS?"
result = rag_chain.invoke({"query": query})
print(result['result'])
```

### Contributors

- **N Padma Priya**
- **Manmohan Reddy**
- **Deepak Gonchikar**
- **Huvishka**
- **Yuvika Singh**

