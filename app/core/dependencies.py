from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
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
from app.citations.service import CitationService


def get_rag_service(db: Session = Depends(get_db)) -> ConversationalRAGService:
    embedding = HuggingFaceEmbeddingService()

    vector_store = PgVectorStore(
        db,
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
            db
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
    
    
    citation_service = CitationService()
    
    # Complete Conversational RAG
    conversational_rag = (
        ConversationalRAGService(
            conversation_service=conversation_service,
            query_rewriter=query_rewriter,
            retrieval_service=retrieval_service,
            generation_service=generation_service,
            context_assembler=context_assembler,
            citation_service=citation_service
        )
    )

    return conversational_rag


def get_conversation_service(db:Session=Depends(get_db)):

    conversation_repository = PostgresConversationRepository( db )
    

    conversation_service = ConversationService( conversation_repository )

    return conversation_service 