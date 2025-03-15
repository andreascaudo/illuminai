from abc import ABC, abstractmethod


class DocumentHandler(ABC):
    """
    Abstract base class for document handlers.

    All document handlers must implement this interface to provide
    a standardized way to read and extract text from different document formats.
    """

    @abstractmethod
    def read(self, file_path):
        """
        Read the document at the given file path and return its content as text.

        Args:
            file_path (str): Path to the document file

        Returns:
            str: The extracted text content of the document

        Raises:
            Exception: If the document cannot be read
        """
        pass

    @classmethod
    def get_supported_extensions(cls):
        """
        Get a list of file extensions supported by this handler.

        Returns:
            list: A list of supported file extensions
        """
        return []
