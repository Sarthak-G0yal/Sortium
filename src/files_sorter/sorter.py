import os
import shutil
from datetime import datetime

"""
This file defines the Sorter class, which helps in organizing files
in a directory based on file type (like Images, Documents, etc.)
and modification date.
"""

# Main sorter class.


class Sorter:
    """
    Initializes the Sorter with a dictionary mapping categories to file extensions.

    Example:
        file_types = {
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Documents": [".pdf", ".docx", ".txt"],
            "Videos": [".mp4", ".avi"],
            "Music": [".mp3", ".wav"],
            "Others": []
        }
    """

    def __init__(self, file_types_dict: dict):
        if not isinstance(file_types_dict, dict):
            raise TypeError("file_types_dict must be a dictionary.")
        self.file_types_dict = file_types_dict

    def get_file_modified_date(self, file_path):
        """
        Returns the last modified datetime of a file.

        :param file_path: Full path to the file.
        :return: datetime object representing last modification time.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")
        return datetime.fromtimestamp(os.stat(file_path).st_mtime)

    def get_category(self, extension: str) -> str:
        """
        Determines the category of a file based on its extension.

        :param extension: File extension (e.g., '.jpg').
        :return: Category name as string.
        """
        for category, extensions in self.file_types_dict.items():
            if extension.lower() in extensions:
                return category
        return "Others"

    def move_it_out(self, folder_path: str, dest_folder_path: str) -> None:
        """
        Moves files from all subdirectories in a folder to a destination folder.
        Then removes those subdirectories.

        :param folder_path: Path containing subdirectories.
        :param dest_folder_path: Path where files should be moved.
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

        :param folder_path: Directory with unsorted files.
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

    def sort_by_date(self, folder_path: str, folder_types: list) -> None:
        """
        Sorts files inside each category folder into subfolders by their last modified date.

        :param folder_path: Root path where category folders exist.
        :param folder_types: List of folder names to process (e.g., ['Images', 'Documents']).
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")
        if not isinstance(folder_types, list):
            raise TypeError("folder_types must be a list of folder type names.")

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
