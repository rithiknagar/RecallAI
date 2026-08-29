from app.embeddings.base import EmbeddingService
from app.retrieval.models import RetrievedChunk
from app.retrieval.retriever import Retriever
from app.vectorstore.base import VectorStore


class PgVectorRetriever(Retriever):

    def __init__(
        self,
        vector_store: VectorStore
    ):
        self._vector_store = vector_store

    def retrieve( self, query: str, top_k: int = 5, ) -> list[RetrievedChunk]:


        return self._vector_store.similarity_search( query, top_k )