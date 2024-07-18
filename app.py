import streamlit as st
from rag import get_rag_chain

# Initialize RAG chain
rag_chain = get_rag_chain()

# Streamlit interface
st.title("Custom LLM Chatbot")
query = st.text_input("Enter your query:")

if query:
    try:
        result = rag_chain.invoke({"query": query})
        st.write(result['result'])
    except Exception as e:
        st.write(f"Error: {e}")
