from app.core.database import SessionLocal

from app.conversation.postgres_repository import (
    PostgresConversationRepository,
)
from app.conversation.service import (
    ConversationService,
)
from app.conversation.ollama_query_rewriter import (
    OllamaQueryRewriter,
)
from app.conversation.rag_query_rewrite_prompt import (
    RAGQueryRewritePromptBuilder,
)

from app.embeddings.huggingface import (
    HuggingFaceEmbeddingService,
)

from app.generation.ollama_llm import OllamaLLM
from app.generation.rag_prompt import RAGPromptBuilder
from app.generation.service import GenerationService

from app.rag.conversational_service import (
    ConversationalRAGService,
)

from app.retrieval.pg_retriever import (
    PgVectorRetriever,
)
from app.retrieval.service import RetrievalService

from app.vectorstore.pgvector_store import (
    PgVectorStore,
)

from app.reranking.huggingface import (
    HuggingFaceReranker,
)

from app.contextassembler.assembler import DefaultContextAssembler


session = SessionLocal()

embedding = HuggingFaceEmbeddingService()

vector_store = PgVectorStore(
    session,
    embedding,
)

retriever = PgVectorRetriever(
    vector_store
)
reranker = HuggingFaceReranker(
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
)

retrieval_service = RetrievalService(
    retriever,
    reranker,
)

llm = OllamaLLM(
    model="gemma3",
    base_url="http://localhost:11434",
)

# Query rewriting
query_rewrite_prompt = (
    RAGQueryRewritePromptBuilder()
)

query_rewriter = OllamaQueryRewriter(
    llm=llm,
    prompt_builder=query_rewrite_prompt,
)

# Conversation persistence
conversation_repository = (
    PostgresConversationRepository(
        session
    )
)

conversation_service = ConversationService(
    conversation_repository
)

# Final answer generation
rag_prompt_builder = RAGPromptBuilder()

generation_service = GenerationService(
    llm=llm,
    prompt_builder=rag_prompt_builder,
)

context_assembler=DefaultContextAssembler()
# Complete Conversational RAG
conversational_rag = (
    ConversationalRAGService(
        conversation_service=conversation_service,
        query_rewriter=query_rewriter,
        retrieval_service=retrieval_service,
        generation_service=generation_service,
        context_assembler=context_assembler
    )
)

session_id = conversation_service.create_session()


print(
    f"Conversation session: {session_id}"
)

def main():

    while True:

        question = input(
            "\nAsk a question "
            "(type exit to quit): "
        )

        if question.strip().lower() == "exit":
            # session.commit()
            break

        response = conversational_rag.ask(
            session_id=session_id,
            question=question,
            top_k=5,
            metadata_filter={
                "filename": "company_letter.pdf"
            },
            candidate_k=10
            
            # similarity_threshold=0.70
           
        )

        print("\nAnswer:")
        print(response.answer)

if __name__ == "__main__":
    main()