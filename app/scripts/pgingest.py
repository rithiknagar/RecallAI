from app.ingestion.chunker import DocumentChunker
from app.embeddings.huggingface import HuggingFaceEmbeddingService
from app.vectorstore.faiss_store import FAISSVectorStore
from app.ingestion.loaders.pdf_loader import PDFDocumentLoader
from app.ingestion.metadata import MetadataBuilder
from app.ingestion.pipeline import IngestionPipeline
from app.repositories.postgres_document_repository import PostgresDocumentRepository
from app.vectorstore.pgvector_store import PgVectorStore
from app.core.database import SessionLocal

def main():
    print("starting")
    session=SessionLocal()

    embedding_service=HuggingFaceEmbeddingService()

    vector_store=PgVectorStore(session,embedding_service)

    loader=PDFDocumentLoader()

    chunker=DocumentChunker()

    metadata=MetadataBuilder()

    

    postgres=PostgresDocumentRepository(session)



    pipeline=IngestionPipeline(loader, chunker,metadata,vector_store,postgres)

    pipeline.ingest(
        file_path=(
            "app/data/documents/company_letter.pdf"
        ),
        document_id="company_letter-v1",
        filename="company_letter.pdf",
    )

    print("Document ingestion completed.")

if __name__=="__main__":
    main()




