from app.ingestion.chunker import DocumentChunker
from app.embeddings.huggingface import HuggingFaceEmbeddingService
from app.vectorstore.faiss_store import FAISSVectorStore
from app.ingestion.loaders.pdf_loader import PDFDocumentLoader
from app.ingestion.metadata import MetadataBuilder
from app.ingestion.pipeline import IngestionPipeline

def main():
    print("starting")
    embedding_service=HuggingFaceEmbeddingService()

    vector_store=FAISSVectorStore(embedding_service)

    loader=PDFDocumentLoader()

    chunker=DocumentChunker()

    metadata=MetadataBuilder()

    pipeline=IngestionPipeline(loader, chunker,metadata,vector_store)

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




