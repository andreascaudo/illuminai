"""
ODT (OpenDocument Text) document handler.
"""
from odf import text, teletype
from odf.opendocument import load


class ODTHandler:
    """Handler for OpenDocument Text (ODT) documents."""

    def __init__(self):
        self.file_path = None
        self.content = ""

    def open_document(self, file_path):
        """
        Open an ODT document and load its content.

        Args:
            file_path (str): Path to the ODT document.

        Returns:
            bool: Whether the document was successfully opened.
        """
        try:
            self.file_path = file_path

            # Load the ODT document
            doc = load(file_path)

            # Extract all paragraphs
            paragraphs = []
            for paragraph in doc.getElementsByType(text.P):
                para_text = teletype.extractText(paragraph)
                if para_text.strip():
                    paragraphs.append(para_text)

            self.content = "\n".join(paragraphs)
            return True

        except Exception as e:
            print(f"Error opening ODT document: {e}")
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
