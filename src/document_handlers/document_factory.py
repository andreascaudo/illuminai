"""
Factory for creating document handlers based on file extension.
"""
import os

from src.document_handlers.pdf_handler import PDFHandler
from src.document_handlers.txt_handler import TXTHandler
from src.document_handlers.docx_handler import DOCXHandler
from src.document_handlers.rtf_handler import RTFHandler
from src.document_handlers.odt_handler import ODTHandler
from src.document_handlers.md_handler import MarkdownHandler


class DocumentFactory:
    """Factory for creating document handlers based on file extension."""

    @staticmethod
    def supported_extensions():
        """
        Get a list of supported file extensions.

        Returns:
            list: List of supported file extensions (with dot prefix).
        """
        return [".pdf", ".txt", ".docx", ".rtf", ".odt", ".md"]

    @staticmethod
    def create_handler(file_path):
        """
        Create a document handler based on the file extension.

        Args:
            file_path (str): Path to the document file.

        Returns:
            DocumentHandler: Handler for the document type or None if unsupported.
        """
        if not os.path.isfile(file_path):
            return None

        extension = os.path.splitext(file_path)[1].lower()

        # Create handler based on file extension
        handler = None
        if extension == ".pdf":
            handler = PDFHandler()
        elif extension == ".txt":
            handler = TXTHandler()
        elif extension == ".docx":
            handler = DOCXHandler()
        elif extension == ".rtf":
            handler = RTFHandler()
        elif extension == ".odt":
            handler = ODTHandler()
        elif extension == ".md":
            handler = MarkdownHandler()

        # Open the document if a handler was created
        if handler and handler.open_document(file_path):
            return handler

        return None
