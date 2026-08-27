from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Production RAG"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_dimension: int = 384

    chunk_size: int = 500
    chunk_overlap: int = 100

    retrieval_top_k: int = 5
    
    database_url: str ="postgresql://postgres:Ragapp%409874@db.uhcogezwtmobfmycidky.supabase.co:5432/postgres"

    faiss_index_path: str = "data/vectorstore/index.faiss"
    documents_path: str = "data/vectorstore/documents.pkl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()