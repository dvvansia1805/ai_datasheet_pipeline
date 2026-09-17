## PDF Ingestion Module for GRAVLOC AI Datasheet Pipeline

This module handles:
1. PDF file discovery from Google Drive
2. PDF download and local storage
3. Text extraction from PDFs
4. Batch processing support
5. Metadata preservation

Author: AI_Developer_GRAVLOC
Date: 2026-09-17

### Features

- **Google Drive Integration**: Download PDFs from Google Drive folders
- **Multiple Extraction Methods**: Text extraction, OCR support, hybrid mode
- **Batch Processing**: Process multiple PDFs efficiently
- **Metadata Preservation**: Full traceability with source URLs, timestamps, confidence scores
- **Error Handling**: Robust error handling with logging

### Classes

- `PDFIngestionPipeline`: Main pipeline for PDF processing
- `PDFMetadata`: Dataclass for document metadata
- `ExtractedContent`: Dataclass for extracted content
- `GoogleDrivePDFFetcher`: Helper for Google Drive file discovery

### Usage

```python
from src.ingestion.pdf_loader import PDFIngestionPipeline

pipeline = PDFIngestionPipeline(output_dir="data/raw")
content = pipeline.process_single_pdf(
    file_id="google_drive_file_id",
    file_name="datasheet.pdf",
    file_size=100000,
    download_url="s3_download_url",
    source_url="https://drive.google.com/file/d/..."
)
pipeline.save_extracted_content(content)
```
