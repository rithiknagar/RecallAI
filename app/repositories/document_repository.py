from abc import ABC, abstractmethod
from uuid import UUID

from app.vectorstore.models import DocumentModel


class DocumentRepository(ABC):

    @abstractmethod
    def find_by_content_hash(
        self,
        content_hash: str,
    ) -> DocumentModel | None:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        filename: str,
        content_hash: str,
        title: str | None = None,
        document_type: str | None = None,
    ) -> DocumentModel:
        raise NotImplementedError