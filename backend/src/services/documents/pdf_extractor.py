import io
import structlog
from PyPDF2 import PdfReader
from services.documents.extractor_interface import IDocumentExtractor

logger = structlog.get_logger(__name__)

class PDFExtractor(IDocumentExtractor):
    def extract_text(self, file_bytes: bytes) -> str:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            logger.error("Failed to extract PDF text", error=str(e))
            raise ValueError("Invalid or corrupted PDF file")

    def supported_mime_types(self) -> list[str]:
        return ["application/pdf"]
