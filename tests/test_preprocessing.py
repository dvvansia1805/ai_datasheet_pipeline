"""Tests for preprocessing module."""

import unittest
import tempfile
import os
import json

from src.preprocessing.ocr_processor import (
    DocumentPreprocessor,
    DocumentQuality,
    DocumentClassification
)
from src.preprocessing.document_classifier import (
    DocumentClassifier,
    ClassificationResult
)


class TestDocumentPreprocessor(unittest.TestCase):
    """Test DocumentPreprocessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = DocumentPreprocessor()
    
    def test_quality_assessment(self):
        """Test document quality assessment."""
        # Create a temporary test image
        import cv2
        import numpy as np
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            test_image = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)
            cv2.imwrite(f.name, test_image)
            temp_path = f.name
        
        try:
            quality = self.preprocessor.assess_quality(temp_path)
            
            self.assertIsInstance(quality, DocumentQuality)
            self.assertGreaterEqual(quality.overall_score, 0.0)
            self.assertLessEqual(quality.overall_score, 1.0)
            self.assertIn(quality.quality_grade, ['A', 'B', 'C', 'D', 'F'])
            
        finally:
            os.unlink(temp_path)
    
    def test_document_classification(self):
        """Test document classification."""
        import cv2
        import numpy as np
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            test_image = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)
            cv2.imwrite(f.name, test_image)
            temp_path = f.name
        
        try:
            classification = self.preprocessor.classify_document(temp_path)
            
            self.assertIsInstance(classification, DocumentClassification)
            self.assertIn(classification.doc_type, ['datasheet', 'manual', 'unknown'])
            self.assertGreaterEqual(classification.confidence, 0.0)
            
        finally:
            os.unlink(temp_path)


class TestDocumentClassifier(unittest.TestCase):
    """Test DocumentClassifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classifier = DocumentClassifier()
    
    def test_datasheet_classification(self):
        """Test datasheet document type classification."""
        text = """
        Datasheet
        Electrical Characteristics
        Absolute Maximum Ratings
        Pin Configuration
        Typical Performance Data
        """
        
        result = self.classifier.classify(text)
        
        self.assertEqual(result.doc_type, 'datasheet')
        self.assertGreater(result.doc_type_confidence, 0.5)
        self.assertTrue(result.is_technical_document)
    
    def test_antenna_category(self):
        """Test antenna component category classification."""
        text = """
        Antenna Specifications
        Gain: 8 dBi
        VSWR: < 1.5
        Impedance: 50 ohms
        Frequency: 2.4 GHz
        """
        
        result = self.classifier.classify(text)
        
        self.assertEqual(result.component_category, 'antenna')
        self.assertGreater(result.category_confidence, 0.5)
    
    def test_manufacturer_extraction(self):
        """Test manufacturer name extraction."""
        text = """
        Mini-Circuits ZFL-500LN+
        Wideband LN Amplifier
        """
        
        result = self.classifier.classify(text)
        
        self.assertEqual(result.manufacturer, 'Mini-Circuits')


class TestQualityGrading(unittest.TestCase):
    """Test quality grade assignment."""
    
    def test_grade_boundaries(self):
        """Test quality grade boundaries."""
        # Test A grade
        quality_a = DocumentQuality(
            overall_score=0.95,
            resolution_dpi=300,
            contrast_score=0.9,
            blur_score=0.1,
            skew_angle=0.0,
            noise_level=0.05,
            text_density=0.2,
            quality_grade='A'
        )
        self.assertEqual(quality_a.quality_grade, 'A')
        
        # Test F grade
        quality_f = DocumentQuality(
            overall_score=0.3,
            resolution_dpi=150,
            contrast_score=0.3,
            blur_score=0.7,
            skew_angle=5.0,
            noise_level=0.4,
            text_density=0.02,
            quality_grade='F'
        )
        self.assertEqual(quality_f.quality_grade, 'F')


if __name__ == '__main__':
    unittest.main()