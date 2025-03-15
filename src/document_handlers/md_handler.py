"""
Markdown document handler.
"""
import markdown


class MarkdownHandler:
    """Handler for Markdown documents."""

    def __init__(self):
        self.file_path = None
        self.content = ""
        self.html_content = ""

    def open_document(self, file_path):
        """
        Open a Markdown document and load its content.

        Args:
            file_path (str): Path to the Markdown document.

        Returns:
            bool: Whether the document was successfully opened.
        """
        try:
            self.file_path = file_path

            # Read the markdown file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                self.content = file.read()

            # Convert markdown to HTML (not displayed but available if needed)
            self.html_content = markdown.markdown(self.content)
            return True

        except Exception as e:
            print(f"Error opening Markdown document: {e}")
            return False

    def get_text(self):
        """
        Get the text content of the document.

        Returns:
            str: Text content of the document.
        """
        return self.content

    def get_html(self):
        """
        Get the HTML representation of the document.

        Returns:
            str: HTML content of the document.
        """
        return self.html_content

    def get_file_path(self):
        """
        Get the file path of the document.

        Returns:
            str: File path of the document.
        """
        return self.file_path
