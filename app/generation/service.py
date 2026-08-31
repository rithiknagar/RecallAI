from app.conversation.models import Message
from app.generation.llm import LLM
from app.generation.prompt import PromptBuilder
from app.retrieval.models import RetrievedChunk


class GenerationService:

    def __init__(
        self,
        llm: LLM,
        prompt_builder: PromptBuilder,
    ):
        self._llm = llm
        self._prompt_builder = prompt_builder

    def generate(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        history: list[Message] | None = None,
    ) -> str:

        prompt = self._prompt_builder.build(
            question=question,
            chunks=chunks,
            history=history or [],
        )

        return self._llm.generate(prompt)