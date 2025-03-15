import os
from .document_handler import DocumentHandler


class MarkdownHandler(DocumentHandler):
    """
    Handler for Markdown documents.
    """

    def read(self, file_path):
        """
        Read a Markdown file and return its content.

        Args:
            file_path (str): Path to the Markdown file

        Returns:
            str: The content of the Markdown file

        Raises:
            Exception: If the Markdown file cannot be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        except UnicodeDecodeError:
            # Try with different encodings if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise Exception(f"Failed to decode Markdown file: {str(e)}")

        except Exception as e:
            raise Exception(f"Failed to read Markdown file: {str(e)}")

    @classmethod
    def get_supported_extensions(cls):
        """
        Get a list of file extensions supported by this handler.

        Returns:
            list: A list of supported file extensions
        """
        return ['.md', '.markdown']
