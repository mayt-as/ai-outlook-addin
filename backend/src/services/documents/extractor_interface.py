from abc import ABC, abstractmethod

class IDocumentExtractor(ABC):
    @abstractmethod
    def extract_text(self, file_bytes: bytes) -> str:
        """Extract text from raw file bytes"""
        pass
    
    @abstractmethod
    def supported_mime_types(self) -> list[str]:
        """Return a list of supported MIME types"""
        pass
