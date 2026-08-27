from langchain_core.documents import Document
from typing import List

class MetadataBuilder:
    def enrich(self, documents:List[Document], document_id :str, filename: str):

        for index, document in enumerate(documents):
            document.metadata.update({
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index
            })

        return documents

