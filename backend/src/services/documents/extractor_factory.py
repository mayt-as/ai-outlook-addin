from typing import Dict, Type, Optional
from services.documents.extractor_interface import IDocumentExtractor
from services.documents.pdf_extractor import PDFExtractor
from services.documents.docx_extractor import DocxExtractor
from services.documents.image_ocr_extractor import ImageOCRExtractor
import structlog

logger = structlog.get_logger(__name__)

class ExtractorFactory:
    def __init__(self):
        self._extractors: Dict[str, IDocumentExtractor] = {}
        self._register_extractor(PDFExtractor())
        self._register_extractor(DocxExtractor())
        self._register_extractor(ImageOCRExtractor())

    def _register_extractor(self, extractor: IDocumentExtractor):
        for mime in extractor.supported_mime_types():
            self._extractors[mime] = extractor

    def get_extractor(self, mime_type: str) -> Optional[IDocumentExtractor]:
        extractor = self._extractors.get(mime_type.lower())
        if not extractor:
            logger.warning("No extractor found for MIME type", mime_type=mime_type)
        return extractor

extractor_factory = ExtractorFactory()
