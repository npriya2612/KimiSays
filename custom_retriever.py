from langchain.schema import BaseRetriever, Document
from typing import List, Any

class CustomRetriever:
    def __init__(self, embedder: Any, vector_index: Any):
        self.embedder = embedder
        self.vector_index = vector_index

    def get_relevant_documents(self, query: str) -> List[Document]:
        query_embedding = self.embedder.embed_text([query])[0]
        relevant_docs = self.vector_index.search(query_embedding, top_k=5)
        return [Document(page_content=doc, metadata={}) for doc in relevant_docs]

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)

class CustomRetrieverWrapper(BaseRetriever):
    def __init__(self, embedder: Any, vector_index: Any):
        super().__init__()
        self.retriever = CustomRetriever(embedder, vector_index)

    def get_relevant_documents(self, query: str) -> List[Document]:
        return self.retriever.get_relevant_documents(query)

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return await self.retriever.aget_relevant_documents(query)
