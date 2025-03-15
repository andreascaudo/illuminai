"""
Text file document handler.
"""


class TXTHandler:
    """Handler for plain text documents."""

    def __init__(self):
        self.file_path = None
        self.content = ""

    def open_document(self, file_path):
        """
        Open a text document and load its content.

        Args:
            file_path (str): Path to the text document.

        Returns:
            bool: Whether the document was successfully opened.
        """
        try:
            self.file_path = file_path
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                self.content = file.read()
            return True
        except Exception as e:
            print(f"Error opening text document: {e}")
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
