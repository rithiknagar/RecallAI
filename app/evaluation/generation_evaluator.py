from app.evaluation.llm_judge import LLMJudge
from app.evaluation.models import EvaluationSample
from app.rag.conversational_service import (
    ConversationalRAGService,
)


class GenerationEvaluator:

    def __init__(
        self,
        rag_service: ConversationalRAGService,
        judge: LLMJudge,
    ) -> None:

        self._rag_service = rag_service
        self._judge = judge

    def evaluate_sample(
        self,
        sample: EvaluationSample,
        session_id
    ) -> dict:

        response = (
            self._rag_service.ask(
                session_id=session_id,
                question=sample.question,
                top_k=5,
            )
        )

        context = "\n\n".join(
            chunk.content
            for chunk in response.retrieved_chunks
        )

        return self._judge.evaluate(
            question=sample.question,
            context=context,
            answer=response.answer,
            reference_answer=sample.expected_answer,
        )

    def evaluate(
            self,
            dataset: list[EvaluationSample],
            session_id,
            k: int = 5,
        ) -> dict[str, float]:
    
            evaluation_response = []
    
            for sample in dataset:
    
                evaluation_response.append(
                    self.evaluate_sample(
                        sample,
                        session_id,
                    )
                )
    
            return evaluation_response
