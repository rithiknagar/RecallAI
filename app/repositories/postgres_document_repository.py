from sqlalchemy import select
from sqlalchemy.orm import Session

from app.vectorstore.models import DocumentModel
from app.repositories.document_repository import (
    DocumentRepository,
)


class PostgresDocumentRepository(
    DocumentRepository
):

    def __init__(self, session: Session):
        self._session = session

    def find_by_content_hash(
        self,
        content_hash: str,
    ) -> DocumentModel | None:

        statement = (
            select(DocumentModel)
            .where(
                DocumentModel.content_hash
                == content_hash
            )
        )

        return self._session.execute(
            statement
        ).scalar_one_or_none()

    def create(
        self,
        filename: str,
        content_hash: str,
        title: str | None = None,
        document_type: str | None = None,
    ) -> DocumentModel:

        document = DocumentModel(
            filename=filename,
            content_hash=content_hash,
            title=title,
            document_type=document_type,
        )

        self._session.add(document)

        self._session.flush()         # No commit

        return document