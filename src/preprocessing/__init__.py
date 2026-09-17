"""Preprocessing Module.

Phase 2: Preprocessing for datasheet pipeline.
- OCR processing (Baidu Unlimited-OCR, Tesseract)
- Document classification
- Language detection
- Quality assessment
"""

from .ocr_processor import (
    OCRResult,
    DocumentQuality,
    DocumentClassification,
    BaiduUnlimitedOCR,
    TesseractOCR,
    DocumentPreprocessor
)

from .document_classifier import (
    ClassificationResult,
    DocumentClassifier
)

__all__ = [
    'OCRResult',
    'DocumentQuality', 
    'DocumentClassification',
    'BaiduUnlimitedOCR',
    'TesseractOCR',
    'DocumentPreprocessor',
    'ClassificationResult',
    'DocumentClassifier'
]