import os
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.core.config import settings
from app.embeddings.base import EmbeddingService
from app.vectorstore.base import VectorStore


class FAISSVectorStore(VectorStore):

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:

        self._embedding_service = embedding_service
        self._store: FAISS | None = None

    def add_documents(
        self,
        documents: List[Document],
    ) -> None:

        texts = [
            document.page_content
            for document in documents
        ]

        metadatas = [
            document.metadata
            for document in documents
        ]

        embeddings = (
            self._embedding_service
            .embed_documents(texts)
        )

        self._store = FAISS.from_embeddings(
            text_embeddings=list(
                zip(texts, embeddings)
            ),
            embedding=self._embedding_service._model,
            metadatas=metadatas,
        )

        os.makedirs(
            os.path.dirname(
                settings.faiss_index_path
            ),
            exist_ok=True,
        )

        self._store.save_local(
            settings.faiss_index_path
        )

    def similarity_search(
        self,
        query: str,
        k: int,
    ) -> List[Document]:

        if self._store is None:
            raise RuntimeError(
                "Vector store has not been initialized."
            )

        return self._store.similarity_search(
            query,
            k=k,
        )