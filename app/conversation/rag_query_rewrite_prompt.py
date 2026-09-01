from app.conversation.models import Message
from app.conversation.query_rewrite_prompt import (
    QueryRewritePromptBuilder,
)


class RAGQueryRewritePromptBuilder(
    QueryRewritePromptBuilder
):

    def build(
        self,
        question: str,
        history: list[Message],
    ) -> str:

        conversation = self._format_history(
            history
        )

        return f"""
You are a query rewriting assistant for a RAG system.

Your job is to rewrite the user's latest question into a
standalone question that can be understood WITHOUT the
conversation history.

Do NOT answer the question.

Use the conversation history to resolve ALL references,
pronouns, and omitted information.

This includes words such as:
- it
- they
- them
- their
- this
- that
- these
- those
- he
- she
- his
- her
- we
- they
- "the same"
- "what about..."
- "how many"
- "can they..."
- "does it..."
- and similar references.

IMPORTANT:
A question is NOT standalone just because it is grammatically
complete.

If the question contains a pronoun or reference whose meaning
depends on the conversation, you MUST replace it with the
actual subject from the conversation.

Examples:

Conversation:
User: How many annual leave days do employees get?
Assistant: Employees get 27 annual leave days.

Latest question:
Can they carry them forward?

Rewrite as:
Can employees carry forward their annual leave days?

Another example:

Conversation:
User: How many annual leave days do employees get?
Assistant: Employees get 27 annual leave days.

Latest question:
How many in a month?

Rewrite as:
How many annual leave days do employees get in a month?

Rules:

1. Preserve the original meaning.
2. Do not answer the question.
3. Resolve references using the conversation.
4. Do not invent information.
5. If the latest question depends on previous messages,
   make it completely self-contained.
6. If the latest question is genuinely standalone,
   return it unchanged.
7. Return ONLY the rewritten question.
8. Do not add explanations.

{conversation}

Latest user question:

{question}

Standalone question:
""".strip()

    def _format_history(
        self,
        history: list[Message],
    ) -> str:

        if not history:
            return "No previous conversation."

        return "\n".join(
            f"{message.role}: {message.content}"
            for message in history
        )