from hashlib import sha256
from typing import List, Tuple

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from app.ingestion.loaders.base import DocumentLoader


class PDFDocumentLoader(DocumentLoader):

    def load(self, file_path: str) -> Tuple[List[Document], str]:

        # Calculate hash of the complete original file
        with open(file_path, "rb") as file:
            file_hash = sha256(file.read()).hexdigest()

        # Load PDF pages using LangChain
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        return documents, file_hash