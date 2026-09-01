from app.conversation.models import Message
from app.conversation.query_rewriter import QueryRewriter
from app.conversation.query_rewrite_prompt import (
    QueryRewritePromptBuilder,
)
from app.generation.llm import LLM


class OllamaQueryRewriter(QueryRewriter):

    def __init__(
        self,
        llm: LLM,
        prompt_builder: QueryRewritePromptBuilder,
    ) -> None:

        self._llm = llm
        self._prompt_builder = prompt_builder

    def rewrite(
        self,
        question: str,
        history: list[Message],
    ) -> str:

        prompt = self._prompt_builder.build(
            question=question,
            history=history,
        )

        rewritten_query = self._llm.generate(
            prompt
        )

        return rewritten_query.strip()