from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from typing import List
from langchain_core.documents import Document

class DocumentChunker():
    def __init__(self):

        self._splitter= RecursiveCharacterTextSplitter( chunk_size=settings.chunk_size,
                                                        chunk_overlap=settings.chunk_overlap  )

    def chunk(self,documents:List[Document])->List[Document]:

        return self._splitter.split_documents(documents)


        