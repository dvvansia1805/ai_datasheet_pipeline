# GRAVLOC AI Datasheet Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**AI/ML pipeline for aerospace component datasheet processing and structured technical data extraction**

---

## 🎯 Mission

Transform unstructured aerospace component documentation (PDFs, images) into accurate, structured, searchable, traceable, and trustworthy technical information for the GRAVLOC Sourcing Companion.

---

## 📊 Pipeline Overview

| Phase | Module | Status | Progress |
|-------|--------|--------|----------|
| **Phase 01** | PDF Ingestion | ✅ Complete | 100% |
| **Phase 02** | Preprocessing | ✅ Complete | 100% |
| **Phase 03** | Table Extraction | 🚧 Planned | 0% |
| **Phase 04** | Field Extraction | 🚧 Planned | 0% |
| **Phase 05** | Normalization | 🚧 Planned | 0% |
| **Phase 06** | Sourcing Companion | 🚧 Planned | 0% |

---

## 📁 Directory Structure

```
ai_datasheet_pipeline/
├── README.md                          # Project overview and documentation
├── .gitignore                         # Python and project exclusions
├── requirements.txt                   # Python dependencies
├── config/
│   ├── pipeline_config.yaml           # Pipeline parameters and settings
│   ├── model_config.yaml              # ML model configurations
│   └── preprocessing_config.yaml      # OCR and preprocessing settings
├── data/
│   ├── raw/                           # Raw datasheet documents (PDFs, images)
│   ├── processed/                     # Processed/extracted data
│   └── schemas/
│       └── datasheet_schema.json      # JSON schema for structured output
├── src/
│   ├── __init__.py
│   ├── ingestion/                     # PDF/image loading module
│   │   ├── __init__.py
│   │   └── pdf_loader.py              # PDF ingestion implementation
│   ├── preprocessing/                 # OCR and classification module
│   │   ├── __init__.py
│   │   ├── ocr_processor.py           # OCR processing (Baidu + Tesseract)
│   │   └── document_classifier.py     # Document classification
│   ├── extraction/                    # Table and field extraction
│   │   └── __init__.py
│   ├── models/                        # ML models and evaluation
│   │   └── __init__.py
│   └── utils/                         # Logging and utilities
│       └── __init__.py
├── tests/                             # Unit and integration tests
│   ├── __init__.py
│   ├── test_pdf_ingestion.py          # Ingestion tests
│   └── test_preprocessing.py          # Preprocessing tests
├── notebooks/                         # Data exploration notebooks
└── docs/                              # Technical documentation
```

---

## 🔧 Installation

### Prerequisites

- Python 3.9 or higher
- Tesseract OCR (for fallback OCR engine)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/dvvansia1805/ai_datasheet_pipeline.git
cd ai_datasheet_pipeline

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (if not already installed)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# macOS:
brew install tesseract

# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

---

## 📥 Phase 01: PDF Ingestion Module

### Overview

The PDF Ingestion Module handles:
- Google Drive integration for bulk PDF access
- Text extraction from text-based PDFs
- OCR extraction from image-based PDFs
- Hybrid extraction (best accuracy)
- Metadata preservation and traceability
- Batch processing support

### Key Classes

```python
from src.ingestion.pdf_loader import PDFIngestionPipeline, PDFMetadata, ExtractedContent

# Initialize pipeline
pipeline = PDFIngestionPipeline()

# Process single PDF
result = pipeline.process_pdf("datasheet.pdf", extraction_method="hybrid")

# Process batch from Google Drive
gdrive_folder_id = "1wL5lx-JVIPp7SebNcaEkqLv9xW6pnJoZ"
results = pipeline.process_google_drive_folder(gdrive_folder_id)
```

### Extraction Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| `text` | Fast text extraction | Text-based PDFs |
| `ocr` | OCR extraction | Image-based PDFs |
| `hybrid` | Combined approach | Default, best accuracy |

### Output Format

```json
{
  "metadata": {
    "file_id": "...",
    "file_name": "antenna_datasheet.pdf",
    "page_count": 5,
    "extracted_text_length": 12500,
    "processing_timestamp": "2026-09-16T21:36:29Z",
    "source_url": "https://drive.google.com/...",
    "extraction_method": "hybrid"
  },
  "pages": [
    {
      "page_number": 1,
      "text": "...",
      "has_ocr": false,
      "confidence": 0.95
    }
  ],
  "text": "Full extracted text..."
}
```

---

## 🧹 Phase 02: Preprocessing Module

### Overview

The Preprocessing Module handles:
- OCR processing with Baidu Unlimited-OCR (primary) and Tesseract (fallback)
- Document classification (type, category, manufacturer)
- Language detection
- Quality assessment and grading

### OCR Processing

#### Supported OCR Engines

| Engine | Type | Status | Description |
|--------|------|--------|-------------|
| **Baidu Unlimited-OCR** | Cloud API | Pluggable | Primary OCR engine (credentials required) |
| **Tesseract OCR** | Local | ✅ Working | Fallback OCR engine |

#### Capabilities

- General text recognition
- Table structure recognition (Baidu)
- Multi-language support (configurable)
- Confidence scoring
- Bounding box extraction

#### Usage

```python
from src.preprocessing.ocr_processor import DocumentPreprocessor

preprocessor = DocumentPreprocessor()

# Process entire PDF
results = preprocessor.process_document("datasheet.pdf", use_ocr=True)

# Process single page
page_result = preprocessor.process_page("datasheet.pdf", page_number=1)

# Quality assessment
quality = preprocessor.assess_quality("image.png")
print(f"Grade: {quality.quality_grade}, Score: {quality.overall_score}")
```

### Document Classification

#### Classification Types

| Type | Method | Status |
|------|--------|--------|
| Document Type | Heuristic-based | ✅ Working |
| Component Category | Heuristic-based | ✅ Working |
| Manufacturer | Keyword extraction | ✅ Working |
| Language | Placeholder | TODO |

#### Supported Categories

- antenna
- connector
- amplifier
- filter
- oscillator
- transceiver
- cable
- adapter
- attenuator
- other

#### Usage

```python
from src.preprocessing.document_classifier import DocumentClassifier

classifier = DocumentClassifier()
result = classifier.classify(extracted_text)

print(f"Type: {result.doc_type}")
print(f"Category: {result.component_category}")
print(f"Manufacturer: {result.manufacturer}")
```

### Quality Assessment

#### Metrics

| Metric | Description | Range |
|--------|-------------|-------|
| **Overall Score** | Composite quality score | 0.0 - 1.0 |
| **Resolution DPI** | Image resolution | 150-600 DPI |
| **Contrast Score** | Image contrast | 0.0 - 1.0 |
| **Blur Score** | Blur detection | 0.0 - 1.0 |
| **Noise Level** | Noise estimation | 0.0 - 1.0 |
| **Text Density** | Text content ratio | 0.0 - 1.0 |

#### Quality Grades

| Grade | Score Range | Action |
|-------|-------------|--------|
| **A** | 0.90 - 1.00 | Process immediately |
| **B** | 0.75 - 0.89 | Process normally |
| **C** | 0.60 - 0.74 | Flag for review |
| **D** | 0.40 - 0.59 | High error risk |
| **F** | 0.00 - 0.39 | Reject/Re-scan |

---

## ⚙️ Configuration

### Preprocessing Configuration

Edit `config/preprocessing_config.yaml`:

```yaml
ocr:
  primary_engine: baidu_unlimited
  fallback_engine: tesseract
  
  baidu:
    api_key: ${BAIDU_API_KEY}
    secret_key: ${BAIDU_API_SECRET}
    
  tesseract:
    languages: "eng"
    dpi: 300

quality_assessment:
  weights:
    contrast: 0.3
    blur: 0.3
    noise: 0.2
    text_density: 0.2
```

### Pipeline Configuration

Edit `config/pipeline_config.yaml`:

```yaml
pipeline:
  supported_formats:
    - pdf
    - png
    - jpg
    - tiff
  
  extraction:
    confidence_threshold: 0.7
    max_pages: 50
    
  output:
    format: json
    include_metadata: true
    include_confidence: true
```

---

## 🔑 Baidu Unlimited-OCR Integration

**Status:** Architecture implemented, API integration pending credentials

### Setup Instructions

1. **Register for Baidu AI Cloud:** https://ai.baidu.com/
2. **Create OCR application** to get API credentials
3. **Set environment variables:**
   ```bash
   export BAIDU_API_KEY="your_api_key"
   export BAIDU_API_SECRET="your_secret_key"
   ```
4. **The OCR processor will automatically use Baidu** as primary engine with Tesseract fallback

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific module tests
python -m pytest tests/test_pdf_ingestion.py -v
python -m pytest tests/test_preprocessing.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

- **test_pdf_ingestion.py:** PDF loading, text extraction, OCR fallback, batch processing
- **test_preprocessing.py:** Quality assessment, classification, OCR processing

---

## 📊 Current Dataset

| Metric | Value |
|--------|-------|
| **Source** | Google Drive (Satbase Antenna Datasheets) |
| **Folder ID** | 1wL5lx-JVIPp7SebNcaEkqLv9xW6pnJoZ |
| **Total PDFs** | 199 |
| **Other Files** | 1 (PNG image) |

---

## 🚀 Next Steps

1. **Phase 03: Table Extraction** - Extract technical tables from datasheets
2. **Phase 04: Field Extraction** - Extract component specifications
3. **Phase 05: Normalization** - Unit normalization and entity resolution
4. **Phase 06: Sourcing Companion** - Deploy user-facing AI companion

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🏢 About GRAVLOC

GRAVLOC is a B2B procurement platform focused on the global space industry. We connect aerospace organizations with space-component suppliers and support component discovery, technical datasheet processing, supplier evaluation, and procurement workflows.

**Website:** https://gravloc.com

---

## 👥 Team

- **AI_Developer_GRAVLOC** - AI/ML pipeline development
- **CTO_GRAVLOC** - Technical architecture and infrastructure
- **CEO_GRAVLOC** - Strategic oversight and coordination

---

## 📞 Contact

For questions or support, please contact the GRAVLOC engineering team.
