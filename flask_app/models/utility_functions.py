import os
import re


class UtilityFunctions:
    """
    Provides utility functions for file handling and text sanitization.
    """

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """
        Creates a directory at the given path if it doesn't already exist.

        Args:
            directory_path (str): The path where the directory should be created.

        Returns:
            None
        """
        os.makedirs(directory_path, exist_ok=True)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitizes the given filename by removing special characters and replacing spaces with underscores.

        Args:
            filename (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        sanitized: str = re.sub(r"[^\w\s-]", "", filename)
        sanitized = re.sub(r"\s+", " ", sanitized).strip()
        sanitized = sanitized.replace(" ", "_")
        return sanitized

    @staticmethod
    def save_to_txt_file(file_path: str, content: str) -> None:
        """
        Saves the given content to a text file at the specified path.

        Args:
            file_path (str): The path where the text file should be saved.
            content (str): The content to save in the text file.

        Returns:
            None
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
