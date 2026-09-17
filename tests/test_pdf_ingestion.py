"""
Test script for PDF Ingestion Module

This script demonstrates how to use the PDF ingestion pipeline
with sample files from Google Drive.

Author: AI_Developer_GRAVLOC
Date: 2026-09-17
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.pdf_loader import PDFIngestionPipeline, ExtractedContent


def test_single_pdf_ingestion():
    """Test ingestion of a single PDF file."""
    print("=" * 60)
    print("TEST: Single PDF Ingestion")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = PDFIngestionPipeline(output_dir="data/raw")
    
    # Sample PDF data (replace with actual Google Drive data)
    sample_pdf = {
        "file_id": "197AM8yF5YK_1xClYGsjuUXnPkPW6G7Bw",
        "file_name": "satbase-chorus01-lp-cubesat-deployable-antenna-datasheet.pdf",
        "file_size": 545073,
        "download_url": "s3_url_from_google_drive_tool",
        "source_url": "https://drive.google.com/file/d/197AM8yF5YK_1xClYGsjuUXnPkPW6G7Bw"
    }
    
    try:
        # Process the PDF
        content: ExtractedContent = pipeline.process_single_pdf(
            file_id=sample_pdf["file_id"],
            file_name=sample_pdf["file_name"],
            file_size=sample_pdf["file_size"],
            download_url=sample_pdf["download_url"],
            source_url=sample_pdf["source_url"]
        )
        
        # Print results
        print(f"\n✓ Successfully processed: {content.metadata.file_name}")
        print(f"  - Pages: {content.metadata.page_count}")
        print(f"  - Text length: {content.metadata.extracted_text_length} characters")
        print(f"  - Has images: {content.metadata.has_images}")
        print(f"  - Extraction method: {content.metadata.extraction_method}")
        
        # Save extracted content
        output_path = pipeline.save_extracted_content(content, output_format="json")
        print(f"  - Saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Failed: {str(e)}")
        return False


def test_batch_ingestion():
    """Test batch ingestion of multiple PDF files."""
    print("\n" + "=" * 60)
    print("TEST: Batch PDF Ingestion")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = PDFIngestionPipeline(output_dir="data/raw")
    
    # Sample batch of PDFs (replace with actual Google Drive data)
    sample_pdfs = [
        {
            "id": "197AM8yF5YK_1xClYGsjuUXnPkPW6G7Bw",
            "name": "satbase-chorus01-lp-cubesat-deployable-antenna-datasheet.pdf",
            "size": 545073,
            "webViewLink": "https://drive.google.com/file/d/197AM8yF5YK_1xClYGsjuUXnPkPW6G7Bw"
        },
        {
            "id": "1oEn1iK6Pr5GYkwIB0d_VNe4g_aiYhCRO",
            "name": "satbase-end-to-end-solution-with-xlink-ax-60-datasheet.pdf",
            "size": 355978,
            "webViewLink": "https://drive.google.com/file/d/1oEn1iK6Pr5GYkwIB0d_VNe4g_aiYhCRO"
        },
        {
            "id": "1-F687WBiZsJdvl8NODvxSy98IMFVjb0P",
            "name": "satbase-xlink-x-datasheet.pdf",
            "size": 398922,
            "webViewLink": "https://drive.google.com/file/d/1-F687WBiZsJdvl8NODvxSy98IMFVjb0P"
        }
    ]
    
    # Add download URLs (would come from Google Drive tool)
    for pdf in sample_pdfs:
        pdf["downloadUrl"] = "s3_url_from_google_drive_tool"
    
    # Progress callback
    def progress_callback(current, total, content):
        print(f"  Progress: {current}/{total} - {content.metadata.file_name}")
    
    try:
        # Process batch
        results = pipeline.process_batch(sample_pdfs, progress_callback=progress_callback)
        
        # Print summary
        print(f"\n✓ Batch processing complete")
        print(f"  - Total files: {len(sample_pdfs)}")
        print(f"  - Successfully processed: {len(results)}")
        print(f"  - Failed: {len(sample_pdfs) - len(results)}")
        
        # Save all results
        for content in results:
            pipeline.save_extracted_content(content, output_format="json")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Failed: {str(e)}")
        return False


def test_text_extraction_only():
    """Test text extraction from a local PDF file."""
    print("\n" + "=" * 60)
    print("TEST: Text Extraction from Local PDF")
    print("=" * 60)
    
    pipeline = PDFIngestionPipeline(output_dir="data/raw")
    
    # Path to local PDF (for testing without Google Drive)
    local_pdf_path = "data/raw/sample.pdf"
    
    try:
        # Extract text
        text, page_details = pipeline.extract_text_from_pdf(local_pdf_path, method="hybrid")
        
        print(f"\n✓ Text extraction complete")
        print(f"  - Total text length: {len(text)} characters")
        print(f"  - Pages processed: {len(page_details)}")
        
        for page in page_details:
            print(f"    - Page {page['page_number']}: {page['text_length']} chars")
            if 'tables_found' in page:
                print(f"      Tables found: {page['tables_found']}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\nPDF Ingestion Module - Test Suite")
    print("=" * 60)
    print("Author: AI_Developer_GRAVLOC")
    print("Date: 2026-09-17")
    print("=" * 60)
    
    results = {
        "single_pdf": test_single_pdf_ingestion(),
        "batch_ingestion": test_batch_ingestion(),
        "text_extraction": test_text_extraction_only()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
