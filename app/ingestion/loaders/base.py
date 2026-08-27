from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class DocumentLoader(ABC):

    @abstractmethod
    def load(self,file_path:str)->List[Document]:
        raise NotImplementedError