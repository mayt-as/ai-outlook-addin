import pytest
from services.documents.extractor_factory import extractor_factory

def test_extractor_factory_routing():
    pdf_ext = extractor_factory.get_extractor("application/pdf")
    assert pdf_ext is not None
    assert type(pdf_ext).__name__ == "PDFExtractor"
    
    docx_ext = extractor_factory.get_extractor("application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert docx_ext is not None
    assert type(docx_ext).__name__ == "DocxExtractor"

    img_ext = extractor_factory.get_extractor("image/png")
    assert img_ext is not None
    assert type(img_ext).__name__ == "ImageOCRExtractor"
    
    unsupported = extractor_factory.get_extractor("audio/mp3")
    assert unsupported is None
