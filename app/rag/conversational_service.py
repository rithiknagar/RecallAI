from uuid import UUID

from app.conversation.query_rewriter import QueryRewriter
from app.conversation.service import ConversationService
from app.generation.service import GenerationService
from app.retrieval.service import RetrievalService


class ConversationalRAGService:

    def __init__(
        self,
        conversation_service: ConversationService,
        query_rewriter: QueryRewriter,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
    ) -> None:

        self._conversation_service = (
            conversation_service
        )

        self._query_rewriter = query_rewriter

        self._retrieval_service = (
            retrieval_service
        )

        self._generation_service = (
            generation_service
        )

    def ask(
        self,
        session_id: UUID,
        question: str,
        top_k: int = 5,
    ) -> str:

            history = (
                self._conversation_service
                .get_history(session_id)
            )

            rewritten_query = (
                self._query_rewriter.rewrite(
                    question=question,
                    history=history,
                )
            )

            print("\nOriginal question:")
            print(question)

            print("\nRewritten retrieval query:")
            print(rewritten_query)

            chunks = (
                self._retrieval_service.retrieve(
                    query=rewritten_query,
                    top_k=top_k,
                )
            )

            # print("\nRetrieved chunks:")
            # for index, chunk in enumerate(
            #     chunks,
            #     start=1,
            # ):
            #     print(
            #         f"\n--- Chunk {index} ---"
            #     )
            #     print(
            #         f"Score: {chunk.score}"
            #     )
            #     print(
            #         f"Content: {chunk.content}"
            #     )

            answer = (
                self._generation_service.generate(
                    question=question,
                    chunks=chunks,
                    history=history,
                )
            )

            self._conversation_service.add_message(
                session_id=session_id,
                role="user",
                content=question,
            )

            self._conversation_service.add_message(
                session_id=session_id,
                role="assistant",
                content=answer,
            )




            return answer