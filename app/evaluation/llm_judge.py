from abc import ABC, abstractmethod


class LLMJudge(ABC):

    @abstractmethod
    def evaluate(
        self,
        question: str,
        context: str,
        answer: str,
        reference_answer: str,
    ) -> dict:
        raise NotImplementedError