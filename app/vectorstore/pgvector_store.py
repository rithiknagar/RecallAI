from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from langchain_core.documents import Document

from app.core.config import settings
from app.embeddings.base import EmbeddingService
from app.vectorstore.base import (
    RetrievalResult,
    VectorStore,
)
from app.retrieval.models import RetrievedChunk
from app.vectorstore.models import (
    DocumentChunkModel,
)

class PgVectorStore(VectorStore):

    def __init__(
        self,
        session: Session,
        embedding_service: EmbeddingService,
    ) -> None:

        self._session = session
        self._embedding_service = (
            embedding_service
        )

    def _to_chunk_model(
    self,
    document: Document,
    vector: list[float],
) -> DocumentChunkModel:

        return DocumentChunkModel(
            document_id=document.metadata["document_id"],
            chunk_index=document.metadata["chunk_index"],
            content=document.page_content,
            chunk_metadata={
                key: value
                for key, value in document.metadata.items()
                if key not in {"document_id", "chunk_index"}
            },
            embedding=vector,
        )

    def add_documents(
    self,
    documents: List[Document],
) -> None:

        texts = [
            document.page_content
            for document in documents
        ]

        print(f"text length is {len(texts)}")

        vectors = (
            self._embedding_service
            .embed_documents(texts)
        )
        for doc in documents:
            print(doc.metadata)
            print()

        chunk_models = [
            self._to_chunk_model(
                document,
                vector,
            )
            for document, vector in zip(
                documents,
                vectors,
            )
        ]
        print(f"chunk_models length{len(chunk_models)}")
        for chunk in chunk_models:
            print(chunk.chunk_metadata)
            print()


        try:

            self._session.add_all(
                chunk_models
            )

            self._session.commit()

        except Exception:

            self._session.rollback()

            raise

    def similarity_search(
    self,
    query: str,
    k: int = 5,
    metadata_filter: dict[str, object] | None = None,
) -> List[RetrievalResult]:

        query_vector = (
            self._embedding_service
            .embed_query(query)
        )
        
        distance = (
            DocumentChunkModel.embedding.cosine_distance(
                query_vector
            )
        )

        statement = select(
            DocumentChunkModel,
            distance.label("distance"),
        )

        if metadata_filter:

            for key, value in metadata_filter.items():

                statement = statement.where(
                    DocumentChunkModel
                    .chunk_metadata[key]
                    .as_string()
                    == str(value)
                )

        statement = (
            statement
            .order_by(distance)
            .limit(k)
        )

        rows = (
            self._session
            .execute(statement)
            .all()
        )

        results = []

        for chunk, distance_value in rows:

            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_index,
                    document_id=chunk.document_id,
                    content=chunk.content,
                    retrieval_score=1 - distance_value,
                    metadata=chunk.chunk_metadata,
                )
            )

        return results