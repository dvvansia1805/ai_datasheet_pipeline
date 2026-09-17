"""
PDF Ingestion Module for GRAVLOC AI Datasheet Pipeline

This module handles:
1. PDF file discovery from Google Drive
2. PDF download and local storage
3. Text extraction from PDFs
4. Batch processing support
5. Metadata preservation

Author: AI_Developer_GRAVLOC
Date: 2026-09-17
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# PDF processing libraries
import fitz  # PyMuPDF
from pdfplumber import open as pdfplumber_open
import pytesseract
from PIL import Image
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PDFMetadata:
    """Metadata for a processed PDF document."""
    file_id: str
    file_name: str
    file_size_bytes: int
    page_count: int
    extracted_text_length: int
    has_images: bool
    processing_timestamp: str
    source_url: str
    extraction_method: str


@dataclass
class ExtractedContent:
    """Extracted content from a PDF."""
    text: str
    pages: List[Dict]
    metadata: PDFMetadata


class PDFIngestionError(Exception):
    """Custom exception for PDF ingestion errors."""
    pass


class PDFIngestionPipeline:
    """
    PDF Ingestion Pipeline for aerospace component datasheets.
    
    Supports:
    - Google Drive integration for file discovery and download
    - Multiple extraction methods (text, OCR)
    - Batch processing
    - Metadata preservation and traceability
    """
    
    def __init__(
        self,
        output_dir: str = "data/raw",
        tesseract_path: Optional[str] = None
    ):
        """
        Initialize the PDF Ingestion Pipeline.
        
        Args:
            output_dir: Directory to store downloaded PDFs
            tesseract_path: Path to Tesseract OCR executable (optional)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tesseract_path = tesseract_path
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        logger.info(f"PDF Ingestion Pipeline initialized. Output dir: {self.output_dir}")
    
    def download_pdf_from_drive(
        self,
        file_id: str,
        file_name: str,
        download_url: str
    ) -> Tuple[bytes, str]:
        """
        Download a PDF file from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            file_name: Original file name
            download_url: S3 URL from Google Drive download tool
        
        Returns:
            Tuple of (file_bytes, saved_file_path)
        
        Raises:
            PDFIngestionError: If download fails
        """
        try:
            import requests
            
            # Fetch from S3 URL
            response = requests.get(download_url, timeout=120)
            response.raise_for_status()
            file_bytes = response.content
            
            # Save to output directory
            safe_name = "".join(c for c in file_name if c not in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
            saved_path = self.output_dir / safe_name
            
            with open(saved_path, 'wb') as f:
                f.write(file_bytes)
            
            logger.info(f"Downloaded PDF: {file_name} ({len(file_bytes)} bytes)")
            return file_bytes, str(saved_path)
            
        except Exception as e:
            error_msg = f"Failed to download PDF {file_id}: {str(e)}"
            logger.error(error_msg)
            raise PDFIngestionError(error_msg)
    
    def extract_text_from_pdf(
        self,
        pdf_path: str,
        method: str = "hybrid"
    ) -> Tuple[str, List[Dict]]:
        """
        Extract text from a PDF file using multiple methods.
        
        Args:
            pdf_path: Path to the PDF file
            method: Extraction method - "text", "ocr", or "hybrid"
        
        Returns:
            Tuple of (full_text, page_details)
        """
        full_text = []
        page_details = []
        has_images = False
        
        try:
            # Method 1: PyMuPDF (fast text extraction)
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                text = page.get_text()
                
                # Check for images
                images = page.get_images()
                if images:
                    has_images = True
                
                page_text = {
                    "page_number": page_num + 1,
                    "text_length": len(text),
                    "has_images": len(images) > 0,
                    "image_count": len(images)
                }
                page_details.append(page_text)
                
                full_text.append(text)
            
            doc.close()
            
            # Method 2: PDFPlumber for table detection (if hybrid)
            if method == "hybrid":
                with pdfplumber_open(pdf_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        if tables:
                            page_details[i]["tables_found"] = len(tables)
                            page_details[i]["table_data"] = tables
            
            return "\n\n".join(full_text), page_details
            
        except Exception as e:
            error_msg = f"Failed to extract text from {pdf_path}: {str(e)}"
            logger.error(error_msg)
            raise PDFIngestionError(error_msg)
    
    def extract_text_with_ocr(
        self,
        pdf_path: str,
        dpi: int = 300
    ) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF using OCR (for image-based PDFs).
        
        Args:
            pdf_path: Path to the PDF file
            dpi: DPI for rendering pages
        
        Returns:
            Tuple of (full_text, page_details)
        """
        full_text = []
        page_details = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Render page to image
                mat = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # Convert to PIL Image
                img = Image.open(io.BytesIO(img_data))
                
                # OCR extraction
                text = pytesseract.image_to_string(img)
                
                page_text = {
                    "page_number": page_num + 1,
                    "text_length": len(text),
                    "extraction_method": "ocr",
                    "dpi": dpi
                }
                page_details.append(page_text)
                
                full_text.append(text)
            
            doc.close()
            
            return "\n\n".join(full_text), page_details
            
        except Exception as e:
            error_msg = f"Failed OCR extraction from {pdf_path}: {str(e)}"
            logger.error(error_msg)
            raise PDFIngestionError(error_msg)
    
    def process_single_pdf(
        self,
        file_id: str,
        file_name: str,
        file_size: int,
        download_url: str,
        source_url: str
    ) -> ExtractedContent:
        """
        Process a single PDF file end-to-end.
        
        Args:
            file_id: Google Drive file ID
            file_name: Original file name
            file_size: File size in bytes
            download_url: S3 URL for downloading
            source_url: Original Google Drive URL
        
        Returns:
            ExtractedContent object with text and metadata
        """
        logger.info(f"Processing PDF: {file_name}")
        
        # Download PDF
        file_bytes, saved_path = self.download_pdf_from_drive(
            file_id, file_name, download_url
        )
        
        # Extract text (hybrid method)
        text, page_details = self.extract_text_from_pdf(saved_path, method="hybrid")
        
        # Create metadata
        metadata = PDFMetadata(
            file_id=file_id,
            file_name=file_name,
            file_size_bytes=file_size,
            page_count=len(page_details),
            extracted_text_length=len(text),
            has_images=any(p.get("has_images", False) for p in page_details),
            processing_timestamp=datetime.utcnow().isoformat(),
            source_url=source_url,
            extraction_method="hybrid"
        )
        
        return ExtractedContent(
            text=text,
            pages=page_details,
            metadata=metadata
        )
    
    def process_batch(
        self,
        pdf_files: List[Dict],
        progress_callback=None
    ) -> List[ExtractedContent]:
        """
        Process a batch of PDF files.
        
        Args:
            pdf_files: List of PDF file metadata dicts
            progress_callback: Optional callback for progress updates
        
        Returns:
            List of ExtractedContent objects
        """
        results = []
        total = len(pdf_files)
        
        for i, pdf_info in enumerate(pdf_files):
            logger.info(f"Processing {i+1}/{total}: {pdf_info['name']}")
            
            try:
                content = self.process_single_pdf(
                    file_id=pdf_info['id'],
                    file_name=pdf_info['name'],
                    file_size=int(pdf_info['size']),
                    download_url=pdf_info.get('downloadUrl', ''),
                    source_url=pdf_info.get('webViewLink', '')
                )
                results.append(content)
                
                if progress_callback:
                    progress_callback(i + 1, total, content)
                    
            except PDFIngestionError as e:
                logger.error(f"Failed to process {pdf_info['name']}: {e}")
                # Continue with next file
                continue
        
        logger.info(f"Batch processing complete. Successfully processed: {len(results)}/{total}")
        return results
    
    def save_extracted_content(
        self,
        content: ExtractedContent,
        output_format: str = "json"
    ) -> str:
        """
        Save extracted content to a file.
        
        Args:
            content: ExtractedContent object
            output_format: "json" or "txt"
        
        Returns:
            Path to saved file
        """
        base_name = Path(content.metadata.file_name).stem
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if output_format == "json":
            output_path = output_dir / f"{base_name}_extracted.json"
            data = {
                "metadata": asdict(content.metadata),
                "pages": content.pages,
                "text": content.text
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            output_path = output_dir / f"{base_name}_extracted.txt"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content.text)
        
        logger.info(f"Saved extracted content to: {output_path}")
        return str(output_path)


# Example Usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = PDFIngestionPipeline(output_dir="data/raw")
    logger.info("PDF Ingestion Module loaded successfully")
