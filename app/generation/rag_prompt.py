from app.conversation.models import Message
from app.generation.prompt import PromptBuilder
from app.retrieval.models import RetrievedChunk


class RAGPromptBuilder(PromptBuilder):

    def build(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        history: list[Message],
    ) -> str:

        context = self._build_context(chunks)
        conversation = self._build_history(history)

        return f"""
You are a helpful assistant.

Answer the user's question using the provided context
and conversation history.

Use the retrieved context as the source of truth.

If the answer cannot be found in the provided context,
say that you don't have enough information.

Conversation history:
{conversation}

Retrieved context:
{context}

Current question:
{question}

Answer:
""".strip()

    def _build_context(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:

        return "\n\n".join(
            chunk.content
            for chunk in chunks
        )

    def _build_history(
        self,
        history: list[Message],
    ) -> str:

        if not history:
            return "No previous conversation."

        return "\n".join(
            f"{message.role}: {message.content}"
            for message in history
        )