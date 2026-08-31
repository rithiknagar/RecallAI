from app.generation.ollama_llm import OllamaLLM
from app.generation.rag_prompt import RAGPromptBuilder
from app.retrieval.service import RetrievalService
from app.vectorstore.pgvector_store import PgVectorStore
from app.retrieval.pg_retriever import PgVectorRetriever
from app.retrieval.service import RetrievalService
from app.embeddings.huggingface import HuggingFaceEmbeddingService
from app.rag.service import RAGService
from app.generation.service import GenerationService
from app.core.database import SessionLocal

session=SessionLocal()

embedding=HuggingFaceEmbeddingService()

vector_store=PgVectorStore(session, embedding)

retriever=PgVectorRetriever(vector_store)

retrieval_service=RetrievalService(retriever)

prompt_builder= RAGPromptBuilder()

llm = OllamaLLM(
    model="gemma3",
    base_url="http://localhost:11434",
)

generation_service= GenerationService(llm,prompt_builder)

rag_service=RAGService(retrieval_service, generation_service)

def main():
    while(True):
        question = input("Ask any question (to exit type exit): ")

        if question.strip().lower() == "exit":
            return 

        answer = rag_service.ask(
            question=question,
            top_k=5,
        )

        print("\nAnswer:")
        print(answer)

main()

