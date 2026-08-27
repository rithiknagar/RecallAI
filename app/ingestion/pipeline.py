from app.ingestion.loaders.base import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.ingestion.metadata import MetadataBuilder
from app.embeddings.base import EmbeddingService
from app.vectorstore.base import VectorStore
from app.repositories.document_repository import DocumentRepository

class IngestionPipeline:

    def __init__( self, loader: DocumentLoader, chunker: DocumentChunker, metadata_builder: MetadataBuilder,  vector_store: VectorStore, document_repository: DocumentRepository ):

        self.loader = loader
        self.chunker = chunker
        self.metadata_builder = metadata_builder
        self.vector_store = vector_store
        self.repository=document_repository


    def ingest(self, document_id :str, file_path:str, filename:str):

        documents, content_hash = self.loader.load(file_path)
        print( f"Loaded documents: {len(documents)}")
        print( f"CONTENT HASH: {content_hash}")

        existing = self.repository.find_by_content_hash(content_hash )

        if existing:
            return existing
        
        document=self.repository.create(filename, content_hash)

        chunks=self.chunker.chunk(documents)
        print( f"created chunks: {len(chunks)}")

        chunks=self.metadata_builder.enrich(chunks, document.id, filename)

        print(chunks[0].page_content)
        print(chunks[0].metadata)
        print(chunks[90].metadata)
        print( f"total chunks: {len(chunks)}")

        self.vector_store.add_documents(chunks)