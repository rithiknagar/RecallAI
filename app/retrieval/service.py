from app.retrieval.models import RetrievedChunk
from app.retrieval.retriever import Retriever


class RetrievalService:

    def __init__(
        self,
        retriever: Retriever,
    ):
        self._retriever = retriever

    def retrieve(self, query: str, top_k: int = 5,) -> list[RetrievedChunk]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        return self._retriever.retrieve(
            query=query,
            top_k=top_k,
        )