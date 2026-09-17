# AI Datasheet Pipeline

AI/ML pipeline for aerospace component datasheet processing and structured technical data extraction for GRAVLOC.

## Overview

This pipeline transforms unstructured aerospace component documentation into accurate, structured, searchable, traceable, and trustworthy technical information.

### Mission

Transform unstructured aerospace component documentation into structured technical data for the GRAVLOC Sourcing Companion.

## Architecture

```
┌─────────────────┐
│  Google Drive   │  ← Source: Antenna Datasheets (199 PDFs)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Ingestion  │  ← Download & Text Extraction
│     Module      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preprocessing   │  ← OCR, Classification
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extraction     │  ← Tables, Fields, Units
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Models        │  ← ML Processing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Structured     │  ← JSON Output
│   Output        │
└─────────────────┘
```

## Current Status

| Component | Status | Description |
|-----------|--------|-------------|
| **Directory Structure** | ✅ Complete | Pipeline modules organized |
| **PDF Ingestion** | ✅ Complete | Google Drive integration, text extraction |
| **Preprocessing** | 🚧 Planned | OCR, document classification |
| **Extraction** | 🚧 Planned | Table and field extraction |
| **Models** | 🚧 Planned | ML model integration |
| **Evaluation** | 🚧 Planned | Model benchmarking |

## Installation

```bash
# Clone repository
git clone https://github.com/dvvansia1805/ai_datasheet_pipeline
cd ai_datasheet_pipeline

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (for OCR support)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr
# macOS:
brew install tesseract
# Windows: Download from https://github.com/tesseract-ocr/tesseract
```

## PDF Ingestion Module

### Features

- **Google Drive Integration**: Download PDFs from Google Drive folders
- **Multiple Extraction Methods**: Text extraction, OCR support, hybrid mode
- **Batch Processing**: Process multiple PDFs efficiently
- **Metadata Preservation**: Full traceability with source URLs, timestamps
- **Error Handling**: Robust error handling with logging

### Usage

```python
from src.ingestion.pdf_loader import PDFIngestionPipeline

# Initialize pipeline
pipeline = PDFIngestionPipeline(output_dir="data/raw")

# Process single PDF
content = pipeline.process_single_pdf(
    file_id="google_drive_file_id",
    file_name="datasheet.pdf",
    file_size=100000,
    download_url="s3_download_url",
    source_url="https://drive.google.com/file/d/..."
)

# Save extracted content
pipeline.save_extracted_content(content, output_format="json")
```

### Output Format

```json
{
  "metadata": {
    "file_id": "google_drive_file_id",
    "file_name": "datasheet.pdf",
    "file_size_bytes": 100000,
    "page_count": 5,
    "extracted_text_length": 12500,
    "has_images": true,
    "processing_timestamp": "2026-09-17T11:19:48Z",
    "source_url": "https://drive.google.com/file/d/...",
    "extraction_method": "hybrid"
  },
  "pages": [
    {
      "page_number": 1,
      "text_length": 2500,
      "has_images": true,
      "image_count": 3,
      "tables_found": 2
    }
  ],
  "text": "Full extracted text from all pages..."
}
```

## Data Sources

### Antenna Datasheets

- **Source**: Google Drive Folder
- **Folder ID**: `1wL5lx-JVIPp7SebNcaEkqLv9xW6pnJoZ`
- **Total PDFs**: 199
- **Format**: PDF
- **Content**: Antenna component datasheets from Satbase

## Directory Structure

```
ai_datasheet_pipeline/
├── README.md                          # Project overview
├── .gitignore                         # Git exclusions
├── requirements.txt                   # Python dependencies
├── config/
│   ├── pipeline_config.yaml           # Pipeline parameters
│   └── model_config.yaml              # ML model configurations
├── data/
│   ├── raw/                           # Downloaded PDFs
│   ├── processed/                     # Extracted data
│   └── schemas/
│       └── datasheet_schema.json      # Output JSON schema
├── src/
│   ├── __init__.py
│   ├── ingestion/                     # ✅ PDF Ingestion Module
│   │   └── pdf_loader.py
│   ├── preprocessing/                 # 🚧 OCR & Classification
│   │   └── __init__.py
│   ├── extraction/                    # 🚧 Table & Field Extraction
│   │   └── __init__.py
│   ├── models/                        # 🚧 ML Models
│   │   └── __init__.py
│   └── utils/                         # Utilities
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_pdf_ingestion.py          # PDF Ingestion tests
├── notebooks/                         # Data exploration
└── docs/                              # Technical documentation
```

## Testing

```bash
# Run PDF ingestion tests
python tests/test_pdf_ingestion.py
```

## Roadmap

### Phase 1: Ingestion (Complete ✅)
- [x] Directory structure
- [x] PDF ingestion from Google Drive
- [x] Text extraction
- [x] Batch processing
- [x] Metadata preservation

### Phase 2: Preprocessing (Planned)
- [ ] OCR for image-based PDFs
- [ ] Document classification
- [ ] Language detection
- [ ] Quality assessment

### Phase 3: Extraction (Planned)
- [ ] Table extraction
- [ ] Field extraction
- [ ] Unit normalization
- [ ] Confidence scoring

### Phase 4: Models (Planned)
- [ ] Document classifier (DistilBERT)
- [ ] Table extractor (Table Transformer)
- [ ] Field extractor (BERT-NER)
- [ ] Model evaluation

### Phase 5: Sourcing Companion (Future)
- [ ] API integration
- [ ] User-facing interface
- [ ] Natural language queries
- [ ] Component comparison

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

Proprietary - GRAVLOC

## Contact

**AI Developer Agent**: AI_Developer_GRAVLOC  
**Role**: AI/ML and datasheet intelligence specialist  
**Repository**: [dvvansia1805/ai_datasheet_pipeline](https://github.com/dvvansia1805/ai_datasheet_pipeline)
