#!/usr/bin/env python3
"""
Unit tests for document handlers.
Run these tests from the project root with: python -m unittest src/tests/test_document_handlers.py
"""
import os
import unittest

from src.document_handlers.document_factory import DocumentFactory
from src.document_handlers.pdf_handler import PDFHandler
from src.document_handlers.txt_handler import TXTHandler
from src.document_handlers.docx_handler import DOCXHandler
from src.document_handlers.rtf_handler import RTFHandler
from src.document_handlers.odt_handler import ODTHandler
from src.document_handlers.md_handler import MarkdownHandler


class TestDocumentHandlers(unittest.TestCase):
    """Test cases for document handlers."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = "test_documents"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        # Path to our sample text file
        self.txt_file = os.path.join(self.test_dir, "sample.txt")

    def test_factory_supported_extensions(self):
        """Test that the document factory returns supported extensions."""
        extensions = DocumentFactory.supported_extensions()
        self.assertIsInstance(extensions, list)
        self.assertTrue(len(extensions) > 0)
        self.assertIn(".txt", extensions)
        self.assertIn(".pdf", extensions)
        self.assertIn(".docx", extensions)
        self.assertIn(".rtf", extensions)
        self.assertIn(".odt", extensions)
        self.assertIn(".md", extensions)

    def test_txt_handler(self):
        """Test the TXT handler."""
        if not os.path.exists(self.txt_file):
            self.skipTest(f"Test file {self.txt_file} not found")

        handler = TXTHandler()
        result = handler.open_document(self.txt_file)
        self.assertTrue(result)

        text = handler.get_text()
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)
        self.assertIn("Sample Text for IlluminAI Document Reader", text)

        file_path = handler.get_file_path()
        self.assertEqual(file_path, self.txt_file)

    def test_document_factory(self):
        """Test the document factory."""
        if not os.path.exists(self.txt_file):
            self.skipTest(f"Test file {self.txt_file} not found")

        handler = DocumentFactory.create_handler(self.txt_file)
        self.assertIsNotNone(handler)
        self.assertIsInstance(handler, TXTHandler)

        text = handler.get_text()
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)


if __name__ == "__main__":
    unittest.main()
