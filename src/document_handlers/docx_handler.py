"""
DOCX document handler.
"""
import docx


class DOCXHandler:
    """Handler for Microsoft Word DOCX documents."""

    def __init__(self):
        self.file_path = None
        self.content = ""

    def open_document(self, file_path):
        """
        Open a DOCX document and load its content.

        Args:
            file_path (str): Path to the DOCX document.

        Returns:
            bool: Whether the document was successfully opened.
        """
        try:
            self.file_path = file_path

            # Extract text using python-docx
            doc = docx.Document(file_path)
            paragraphs = []

            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)

            self.content = "\n".join(paragraphs)
            return True

        except Exception as e:
            print(f"Error opening DOCX document: {e}")
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
