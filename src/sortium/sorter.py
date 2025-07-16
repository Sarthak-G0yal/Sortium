import shutil
from pathlib import Path
from .file_utils import FileUtils
from .config import DEFAULT_FILE_TYPES
from typing import Dict, List
import re
from concurrent.futures import ProcessPoolExecutor, as_completed


def move_file_by_type(file_path_str: str, category: str, folder_path_str: str) -> str:
    try:
        file_path = Path(file_path_str)
        folder_path = Path(folder_path_str)
        dest_folder = folder_path / category
        dest_folder.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(dest_folder / file_path.name))
        return ""
    except Exception as e:
        return f"Error moving file '{file_path_str}': {e}"


class Sorter:
    """
    Module defining the Sorter class for organizing files within directories.

    The Sorter class provides methods to sort files based on their type,
    modification date, and custom regex patterns. It can categorize files
    into folders, organize them by last modified date and sort files using
    user-defined regex patterns.

    Attributes:
        file_types_dict (Dict[str, List[str]]): A mapping of file category names
            (e.g., "Images", "Documents") to lists of associated file extensions
            (e.g., [".jpg", ".png"]). Used to classify files during sorting. Defaults
            to `DEFAULT_FILE_TYPES` if not provided.
    """

    def __init__(
        self,
        file_types_dict: Dict[str, List[str]] = None,
        file_utils: FileUtils = None,
    ):
        """
        Initializes an instance of the Sorter class.

        Args:
            file_types_dict (Dict[str, List[str]], optional): A dictionary mapping file category names to lists of associated file extensions. Defaults to DEFAULT_FILE_TYPES if not provided.
            file_utils (FileUtils, optional): An instance of FileUtils to use for file utilities. Defaults to FileUtils() if not provided.
        """
        self.file_types_dict = file_types_dict or DEFAULT_FILE_TYPES
        self.file_utils = file_utils or FileUtils()
        self.extension_to_category = {
            ext.lower(): category
            for category, extensions in self.file_types_dict.items()
            for ext in extensions
        }

    def __get_category(self, extension: str) -> str:
        """
        Determines the category of a file based on its extension.

        Args:
            extension (str) : The extension of the file that will be sorted.

        Returns:
            str: Category of the file based on the file_types_dict.
        """
        return self.extension_to_category.get(extension.lower(), "Others")

    def sort_by_type(
        self, folder_path: str, ignore_dir: List[str] | None = None
    ) -> None:
        """
        Sorts files in a directory into subdirectories by file type.

        Args:
            folder_path (str): Path to the directory containing unsorted files.
            ignore_dir (List[str]): Names of subdirectories within `folder_path` that should be ignored during processing.

        Raises:
            FileNotFoundError: If the specified folder does not exist.
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"The path '{folder}' does not exist.")

        try:
            sub_dir_list = self.file_utils.iter_files_and_sub_dirs(
                str(folder), ignore_dir
            )
            for sub_dir_name in sub_dir_list:
                file_path = folder / sub_dir_name

                if file_path.is_file():
                    category = self.__get_category(file_path.suffix)
                    dest_folder = folder / category
                    dest_folder.mkdir(parents=True, exist_ok=True)

                    try:
                        shutil.move(str(file_path), str(dest_folder / file_path.name))
                    except Exception as e:
                        print(f"Error moving file '{file_path.name}': {e}")
        except Exception as e:
            print(f"An error occurred while sorting by type: {e}")

    def sort_by_type_parallel(
        self, folder_path: str, ignore_dir: List[str] | None = None
    ) -> None:
        """
        Sorts files in a directory into subdirectories by file type using multiprocessing.

        Args:
            folder_path (str): Path to the directory containing unsorted files.
            ignore_dir (List[str], optional): Names of subdirectories within `folder_path` to ignore.

        Raises:
            FileNotFoundError: If the specified folder does not exist.
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"The path '{folder}' does not exist.")

        if ignore_dir is None:
            ignore_dir = []

        file_utils = self.file_utils
        tasks = []
        for sub_dir_name in file_utils.iter_files_and_sub_dirs(str(folder), ignore_dir):
            file_path = folder / sub_dir_name
            if not file_path.is_file():
                continue
            category = self.__get_category(file_path.suffix)
            tasks.append((str(file_path), category, str(folder)))

        with ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(move_file_by_type, fp, cat, folder_str)
                for fp, cat, folder_str in tasks
            ]
            for future in as_completed(futures):
                error = future.result()
                if error:
                    print(error)

    def sort_by_date(self, folder_path: str, folder_types: List[str]) -> None:
        """
        Sorts files inside specified category folders into subfolders based on their last modified date.

        Each file is moved into a subfolder named by the modification date in the format "DD-MMM-YYYY".

        Args:
            folder_path (str): Root directory path containing the category folders.
            folder_types (List[str]): List of category folder names to process (e.g., ['Images', 'Documents']).

        Raises:
            FileNotFoundError: If the root folder (`folder_path`) does not exist.

        Notes:
            - If a category folder in `folder_types` does not exist, it will be skipped with a printed message.
            - Errors during moving individual files are caught and printed but do not stop the process.
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"The folder path '{folder}' does not exist.")
        for folder_type in folder_types:
            sub_folder = folder / folder_type
            if sub_folder.exists():
                try:
                    for file_path in sub_folder.iterdir():
                        if file_path.is_file():
                            try:
                                # Get modified date and format it
                                modified = self.file_utils.get_file_modified_date(
                                    str(file_path)
                                )
                                date_folder = sub_folder / modified.strftime("%d-%b-%Y")

                                # Create a subfolder for the date and move the file
                                date_folder.mkdir(parents=True, exist_ok=True)
                                shutil.move(
                                    str(file_path), str(date_folder / file_path.name)
                                )
                            except Exception as e:
                                print(
                                    f"Error sorting file '{file_path.name}' by date: {e}"
                                )
                except Exception as e:
                    print(
                        f"An error occurred while processing folder '{sub_folder}': {e}"
                    )
            else:
                print(f"Sub-folder '{sub_folder}' not found, skipping.")

    def sort_by_regex(
        self, folder_path: str, regex: Dict[str, str], dest_folder_path: str
    ) -> None:
        """
        Sorts files in a directory (recursively) into category subfolders based on matching regex patterns.

        Args:
            folder_path (str): Path to the directory containing unsorted files.
            regex (Dict[str, str]): A dictionary mapping category names to single regex patterns. The name of the category will be used as the subfolder name.
            dest_folder_path (str): Path to the base directory where sorted files will be moved.

        Raises:
            FileNotFoundError: If the specified folder does not exist.
            RuntimeError: If an error occurs during sorting.
        """
        source_path = Path(folder_path)
        dest_base_path = Path(dest_folder_path)

        if not source_path.exists():
            raise FileNotFoundError(f"The path '{source_path}' does not exist.")

        try:
            for item in source_path.iterdir():
                if item.is_file():
                    for category, pattern in regex.items():
                        if re.match(pattern, item.name):
                            dest_folder = dest_base_path / category
                            dest_folder.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(item), str(dest_folder / item.name))
                            break

            for subdir in source_path.iterdir():
                if subdir.is_dir():
                    self.sort_by_regex(str(subdir), regex, str(dest_base_path))

        except Exception as e:
            raise RuntimeError(f"An error occurred while sorting files: {e}")
