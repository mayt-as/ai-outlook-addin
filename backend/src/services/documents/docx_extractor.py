import io
import structlog
import docx
from services.documents.extractor_interface import IDocumentExtractor

logger = structlog.get_logger(__name__)

class DocxExtractor(IDocumentExtractor):
    def extract_text(self, file_bytes: bytes) -> str:
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error("Failed to extract DOCX text", error=str(e))
            raise ValueError("Invalid or corrupted DOCX file")

    def supported_mime_types(self) -> list[str]:
        return ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
