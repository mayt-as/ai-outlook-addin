import io
import structlog
import pytesseract
from PIL import Image
from services.documents.extractor_interface import IDocumentExtractor

logger = structlog.get_logger(__name__)

class ImageOCRExtractor(IDocumentExtractor):
    def extract_text(self, file_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error("Failed to OCR image", error=str(e))
            raise ValueError("Invalid or unreadable image file")

    def supported_mime_types(self) -> list[str]:
        return ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp"]
