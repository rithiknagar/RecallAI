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

        context = self.build_context(chunks)
        conversation = self._build_history(history)

        return f"""
You are a helpful assistant answering questions using the provided context.

Use only the provided context to answer factual questions.

Each context source has a source identifier such as [S1], [S2], etc.

When making a factual claim based on a source, include the corresponding
source identifier in the answer.

Example:
Employees can carry forward up to 5 days of unused leave. [S1]

Rules:
1. Do not invent source identifiers.
2. Only use source identifiers that appear in the provided context.
3. Do not invent information that is not supported by the context.
4. If the context does not contain enough information, say so.
5. Place citations close to the claim they support.

Conversation history:
{conversation}

Retrieved context:
{context}

Current question:
{question}

Answer:
""".strip()

    # def _build_context(
    #     self,
    #     chunks: list[RetrievedChunk],
    # ) -> str:

    #     return "\n\n".join(
    #         chunk.content
    #         for chunk in chunks
    #     )

    def build_context(
    self,
    chunks: list[RetrievedChunk],
) -> str:

        sections = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            source_id = f"S{index}"

            source = chunk.metadata.get(
                "source",
                "unknown",
            )

            page = chunk.metadata.get(
                "page",
                "unknown",
            )

            sections.append(
                f"""
    [{source_id}]
    Document: {source}
    Page: {page}

    {chunk.content}
    """.strip()
            )

        return "\n\n".join(sections)

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