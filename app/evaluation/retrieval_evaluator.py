from app.evaluation.models import EvaluationSample
from app.retrieval.service import RetrievalService


class RetrievalEvaluator:

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:

        self._retrieval_service = (
            retrieval_service
        )

    def recall_at_k(
        self,
        sample: EvaluationSample,
        k: int,
    ) -> float:

        results = self._retrieval_service.retrieve(
            query=sample.question,
            top_k=k,
        )

        retrieved_ids = {
            chunk.chunk_id
            for chunk in results
        }

        relevant_retrieved = (
            retrieved_ids
            & sample.relevant_chunk_ids
        )

        return (
            len(relevant_retrieved)
            / len(sample.relevant_chunk_ids)
        )

    def precision_at_k(
        self,
        sample: EvaluationSample,
        k: int,
    ) -> float:

        results = self._retrieval_service.retrieve(
            query=sample.question,
            top_k=k,
        )

        retrieved_ids = {
            chunk.chunk_id
            for chunk in results
        }

        relevant_retrieved = (
            retrieved_ids
            & sample.relevant_chunk_ids
        )

        if not retrieved_ids:
            return 0.0

        return (
            len(relevant_retrieved)
            / len(retrieved_ids)
        )

    def reciprocal_rank(
        self,
        sample: EvaluationSample,
    ) -> float:

        results = self._retrieval_service.retrieve(
            query=sample.question,
            top_k=10,
        )

        for rank, chunk in enumerate(
            results,
            start=1,
        ):

            if chunk.chunk_id in sample.relevant_chunk_ids:
                return 1 / rank

        return 0.0

    def evaluate(
        self,
        dataset: list[EvaluationSample],
        k: int = 5,
    ) -> dict[str, float]:

        recalls = []
        precisions = []
        reciprocal_ranks = []

        for sample in dataset:

            recalls.append(
                self.recall_at_k(
                    sample,
                    k,
                )
            )

            precisions.append(
                self.precision_at_k(
                    sample,
                    k,
                )
            )

            reciprocal_ranks.append(
                self.reciprocal_rank(
                    sample,
                )
            )

        return {
            "recall_at_k": (
                sum(recalls) / len(recalls)
            ),
            "precision_at_k": (
                sum(precisions) / len(precisions)
            ),
            "mrr": (
                sum(reciprocal_ranks)
                / len(reciprocal_ranks)
            ),
        }