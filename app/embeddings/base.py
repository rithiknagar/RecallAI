from abc import ABC, abstractmethod
from typing import List


class EmbeddingService(ABC):

    @abstractmethod
    def embed_documents( self,texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def embed_query( self, text: str) -> List[float]:
        raise NotImplementedError

# Any embedding implementation must provide these methods.