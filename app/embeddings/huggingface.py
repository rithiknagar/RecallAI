from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
from app.embeddings.base import EmbeddingService

class HuggingFaceEmbeddingService( EmbeddingService ):

    def __init__(self):

        self._model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )

    def embed_documents( self, texts: List[str] ) -> List[List[float]]:

        return self._model.embed_documents(texts)

    def embed_query( self, text: str ) -> List[float]:

        return self._model.embed_query(text)