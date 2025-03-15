import re


class RTFHandler:
    """
    Handler for Rich Text Format (RTF) documents.

    This is a simplified implementation using regex to extract plain text
    from RTF documents without external dependencies.
    """

    def __init__(self):
        self.file_path = None
        self.content = ""

    def open_document(self, file_path):
        """
        Open an RTF document and load its content.

        Args:
            file_path (str): Path to the RTF document.

        Returns:
            bool: Whether the document was successfully opened.
        """
        try:
            self.file_path = file_path
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                rtf_content = file.read()

            # Extract plain text from RTF using our custom parser
            self.content = self._extract_text_from_rtf(rtf_content)
            return True
        except Exception as e:
            print(f"Error opening RTF document: {e}")
            return False

    def _extract_text_from_rtf(self, rtf_content):
        """
        Extract plain text from RTF content.

        Args:
            rtf_content (str): RTF document content

        Returns:
            str: Plain text extracted from RTF
        """
        # This is a simplified RTF parser that extracts plain text
        # It won't handle all RTF features but works for basic documents

        # If the document doesn't start with {\rtf, it might not be a valid RTF file
        if not rtf_content.startswith('{\\rtf'):
            return "Not a valid RTF document."

        # Remove RTF control words and groups
        # 1. Remove control words (starting with backslash)
        text = re.sub(r'\\[a-zA-Z0-9]+(-?[0-9]+)?[ ]?', ' ', rtf_content)

        # 2. Remove hexadecimal values (Unicode characters)
        text = re.sub(r'\\\'[0-9a-fA-F]{2}', '', text)

        # 3. Remove curly braces and their contents if they contain control words
        # This is simplified and won't handle nested braces properly
        text = re.sub(r'{\\*.*?}', '', text)

        # 4. Replace \par with newlines
        text = text.replace('\\par', '\n')

        # 5. Remove remaining curly braces
        text = re.sub(r'[{}]', '', text)

        # 6. Handle line breaks and special characters
        text = text.replace('\\line', '\n')
        text = text.replace('\\tab', '\t')

        # 7. Clean up excess whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text

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

    @classmethod
    def get_supported_extensions(cls):
        """
        Get a list of file extensions supported by this handler.

        Returns:
            list: A list of supported file extensions
        """
        return ['.rtf']
