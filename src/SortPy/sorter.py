import os
import shutil
from datetime import datetime

"""
This module defines the Sorter class for organizing files within directories.

The Sorter class helps sort files based on their type (e.g., Images, Documents)
and their last modification date. It can move files into categorized folders,
further organize them by modification date, and flatten nested directories by
moving files out.
"""

# Main sorter class.


class Sorter:
    """
    Sorter class to organize files in a directory by file type and modification date.

    Attributes:
        file_types_dict (dict[str, list[str]]): A dictionary mapping categories to file extensions.

    Example:
        file_types = {
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Documents": [".pdf", ".docx", ".txt"],
            "Videos": [".mp4", ".avi"],
            "Music": [".mp3", ".wav"],
            "Others": []
        }

        sorter = Sorter(file_types)
        sorter.sort_by_type('/path/to/downloads')
        sorter.sort_by_date('/path/to/downloads', ['Images', 'Documents'])
    """

    def __init__(self, file_types_dict: dict[str, list[str]]):
        self.file_types_dict = file_types_dict

    def get_file_modified_date(self, file_path: str) -> datetime:
        """
        Returns the last modified datetime of a file.

        Args:
            file_path (str): Full path to the file.

        Returns:
            datetime: Datetime object representing the last modification time.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")
        return datetime.fromtimestamp(os.stat(file_path).st_mtime)

    def get_category(self, extension: str) -> str:
        """
        Determines the category of a file based on its extension.

        Args:
            extension (str) : The extension of the file that will be sorted.

        Returns:
            str: Category of the file based on the file_types_dict.
        """
        for category, extensions in self.file_types_dict.items():
            if extension.lower() in extensions:
                return category
        return "Others"

    def flatten_the_dir(self, folder_path: str, dest_folder_path: str) -> None:
        """
        Moves all files from subdirectories of a given folder into a destination folder,
        and then removes those subdirectories.

        This is useful for flattening a directory structure by collecting all files
        from nested folders and moving them into one target folder.

        Args:
            folder_path (str): Path to the root folder containing subdirectories with files.
            dest_folder_path (str): Path to the folder where all files should be moved.

        Raises:
            FileNotFoundError: If the root folder (`folder_path`) does not exist.

        Notes:
            - Any errors encountered while moving files or removing subdirectories are
            caught and printed, but not raised.
            - Fails silently (with printed messages) on permission issues, missing files,
            or non-empty directories during deletion.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

        if not os.path.exists(dest_folder_path):
            os.makedirs(dest_folder_path)

        try:
            # Identify subdirectories within the given folder
            sub_dir_list = [
                name
                for name in os.listdir(folder_path)
                if os.path.isdir(os.path.join(folder_path, name))
            ]
            for sub_dir_name in sub_dir_list:
                file_path = os.path.join(folder_path, sub_dir_name)
                items = os.listdir(file_path)
                for item in items:
                    source_item = os.path.join(file_path, item)
                    dest_item = os.path.join(dest_folder_path, item)
                    try:
                        shutil.move(source_item, dest_item)
                    except Exception as e:
                        print(f"Failed to move '{source_item}' to '{dest_item}': {e}")
                try:
                    os.rmdir(file_path)
                except OSError as e:
                    print(f"Could not remove directory '{file_path}': {e}")
        except Exception as e:
            print(f"Error occurred while cleaning up folders: {e}")

    def sort_by_type(self, folder_path: str) -> None:
        """
        Sorts files in a directory into subdirectories by file type.

        Args:
            folder_path (str): Path to the directory containing unsorted files.

        Raises:
            FileNotFoundError: If the specified folder does not exist.
        """

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The path '{folder_path}' does not exist.")

        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    category = self.get_category(ext)

                    dest_folder = os.path.join(folder_path, category)
                    os.makedirs(dest_folder, exist_ok=True)

                    try:
                        shutil.move(file_path, os.path.join(dest_folder, filename))
                    except Exception as e:
                        print(f"Error moving file '{filename}': {e}")
        except Exception as e:
            print(f"An error occurred while sorting by type: {e}")

    def sort_by_date(self, folder_path: str, folder_types: list[str]) -> None:
        """
        Sorts files inside specified category folders into subfolders based on their last modified date.

        Each file is moved into a subfolder named by the modification date in the format "DD-MMM-YYYY".

        Args:
            folder_path (str): Root directory path containing the category folders.
            folder_types (list[str]): List of category folder names to process (e.g., ['Images', 'Documents']).

        Raises:
            FileNotFoundError: If the root folder (`folder_path`) does not exist.

        Notes:
            - If a category folder in `folder_types` does not exist, it will be skipped with a printed message.
            - Errors during moving individual files are caught and printed but do not stop the process.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")
        for folder_type in folder_types:
            sub_folder_path = os.path.join(folder_path, folder_type)
            if os.path.exists(sub_folder_path):
                try:
                    for filename in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, filename)
                        if os.path.isfile(file_path):
                            try:
                                # Get modified date and format it
                                modified = self.get_file_modified_date(file_path)
                                date_folder = modified.strftime("%d-%b-%Y")

                                # Create a subfolder for the date and move the file
                                dest_folder = os.path.join(sub_folder_path, date_folder)
                                os.makedirs(dest_folder, exist_ok=True)
                                shutil.move(
                                    file_path, os.path.join(dest_folder, filename)
                                )
                            except Exception as e:
                                print(f"Error sorting file '{filename}' by date: {e}")
                except Exception as e:
                    print(
                        f"An error occurred while processing folder '{sub_folder_path}': {e}"
                    )
            else:
                print(f"Sub-folder '{sub_folder_path}' not found, skipping.")
