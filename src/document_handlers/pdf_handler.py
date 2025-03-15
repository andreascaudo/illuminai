"""
PDF document handler with visual rendering capability.
"""
from PyPDF2 import PdfReader

# Try to import fitz (PyMuPDF) for visual rendering
try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available. Visual PDF rendering will be disabled.")


class PDFHandler:
    """Handler for PDF documents with visual rendering capability."""

    def __init__(self):
        self.file_path = None
        self.content = ""
        self.visual_rendering_supported = PYMUPDF_AVAILABLE
        self.document = None  # For visual rendering (PyMuPDF document)

    def open_document(self, file_path):
        """
        Open a PDF document and load its content.

        Args:
            file_path (str): Path to the PDF document.

        Returns:
            bool: Whether the document was successfully opened.
        """
        try:
            self.file_path = file_path

            # Try to open with PyMuPDF for visual rendering
            if PYMUPDF_AVAILABLE:
                try:
                    self.document = fitz.open(file_path)

                    # Extract text with PyMuPDF if available
                    text_content = []
                    for page_num in range(len(self.document)):
                        page = self.document[page_num]
                        text_content.append(page.get_text())

                    self.content = "\n\n".join(text_content)
                    return True

                except Exception as e:
                    print(
                        f"Error opening PDF with PyMuPDF: {e}, falling back to PyPDF2")
                    self.document = None

            # Fall back to PyPDF2 for text extraction only
            reader = PdfReader(file_path)
            text_content = []

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text_content.append(page.extract_text())

            self.content = "\n\n".join(text_content)
            return True

        except Exception as e:
            print(f"Error opening PDF document: {e}")
            return False

    def get_text(self):
        """
        Get the text content of the document.

        Returns:
            str: Text content of the document.
        """
        return self.content

    def get_file_path(self):
        """
        Get the file path of the document.

        Returns:
            str: File path of the document.
        """
        return self.file_path

    def supports_visual_rendering(self):
        """
        Check if this document supports visual rendering.

        Returns:
            bool: Whether visual rendering is supported.
        """
        return self.visual_rendering_supported and self.document is not None

    def get_visual_document(self):
        """
        Get the PyMuPDF document object for visual rendering.

        Returns:
            fitz.Document: The PyMuPDF document or None if not available.
        """
        return self.document
