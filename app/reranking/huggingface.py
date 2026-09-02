from sentence_transformers import CrossEncoder

from app.reranking.base import Reranker
from app.retrieval.models import RetrievedChunk


class HuggingFaceReranker(Reranker):

    def __init__(
        self,
        model_name: str,
    ) -> None:

        self._model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        top_k: int,
    ) -> list[RetrievedChunk]:

        if not chunks:
            return []

        pairs = [
            (query, chunk.content)
            for chunk in chunks
        ]

        scores = self._model.predict(
            pairs
        )

        ranked_chunks = sorted(
            zip(chunks, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        results = []

        for chunk, score in ranked_chunks[:top_k]:

            chunk.rerank_score = float(score)

            results.append(chunk)

        return results