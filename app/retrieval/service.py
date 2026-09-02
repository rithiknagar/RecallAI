from app.retrieval.models import RetrievedChunk
from app.retrieval.retriever import Retriever
from app.reranking.base import Reranker


class RetrievalService:

    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker | None = None,
    ):
        self._retriever = retriever
        self._reranker = reranker

    def retrieve(self, query: str, top_k: int = 5, similarity_threshold: float | None = None, metadata_filter: dict[str, object] | None = None,candidate_k: int | None = None,) -> list[RetrievedChunk]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )
        retrieval_k = (
            candidate_k
            if candidate_k is not None
            else top_k
        )

        chunks= self._retriever.retrieve(
            query=query,
            top_k=retrieval_k,
            metadata_filter=metadata_filter,
        )
        if similarity_threshold is not None:

            chunks = [
                chunk
                for chunk in chunks
                if chunk.retrieval_score >= similarity_threshold
            ]

        if self._reranker is not None:

            chunks = self._reranker.rerank(
                query=query,
                chunks=chunks,
                top_k=top_k,
            )

        else:

            chunks = chunks[:top_k]

        return chunks
    