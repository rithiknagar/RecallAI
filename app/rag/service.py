from app.generation.service import GenerationService
from app.retrieval.service import RetrievalService


class RAGService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
    ):
        self._retrieval_service = retrieval_service
        self._generation_service = generation_service

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        chunks = self._retrieval_service.retrieve(
            query=question,
            top_k=top_k,
        )

        return self._generation_service.generate(
            question=question,
            chunks=chunks,
        )