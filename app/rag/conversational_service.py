from uuid import UUID

from app.conversation.query_rewriter import QueryRewriter
from app.conversation.service import ConversationService
from app.generation.service import GenerationService
from app.retrieval.service import RetrievalService
from app.contextassembler.assembler import ContextAssembler
from app.retrieval.models import RAGResponse


class ConversationalRAGService:

    def __init__(
        self,
        conversation_service: ConversationService,
        query_rewriter: QueryRewriter,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
        context_assembler: ContextAssembler
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
        self._context_assembler = (
            context_assembler
        )

    def ask(
        self,
        session_id: UUID,
        question: str,
        top_k: int = 5,
        similarity_threshold :float | None= None,
        metadata_filter: dict[str, object] | None = None,
        candidate_k: int | None = None,
    ) -> RAGResponse:

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
                    similarity_threshold=similarity_threshold,
                    metadata_filter=metadata_filter,
                    candidate_k=candidate_k
                )
            )
            chunks=self._context_assembler.assemble(chunks)

            # print("\nRetrieved chunks:")
            # for index, chunk in enumerate(
            #     chunks,
            #     start=1,
            # ):
            #     print(
            #         f"\n--- Chunk {index} ---"
            #     )
            #     print(
            #         f"Score: {chunk.retrieval_score}"
            #     )
            #     print(
            #        f"Rerank score: {chunk.rerank_score}"
            #     )
            #     print(
            #          f"chunk_index: {chunk.chunk_id}"
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


            return  RAGResponse(
                answer=answer,
                retrieved_chunks=chunks,
            )