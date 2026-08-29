from app.vectorstore.pgvector_store import PgVectorStore
from app.retrieval.pg_retriever import PgVectorRetriever
from app.retrieval.service import RetrievalService
from app.embeddings.huggingface import HuggingFaceEmbeddingService
from app.core.database import SessionLocal

def main():

    print("starting retriever")

    session=SessionLocal()

    embedding= HuggingFaceEmbeddingService()

    vector_store=PgVectorStore(session, embedding)

    retriever=PgVectorRetriever(vector_store)

    retrieval_service = RetrievalService(retriever)

    query="How many monthly  leaves do employess get ?"

    results=retrieval_service.retrieve(query,5)

    for result in results:

        print("=" * 80)

        print(
            f"Score: {result.score:.4f}"
        )

        print(
            f"Document: {result.document_id}"
        )

        print(
            f"Content:\n{result.content}"
        )

        print(
            f"Metadata: {result.metadata}"
        )

    print("Document retriever completed.")

if __name__=="__main__":
    main()
