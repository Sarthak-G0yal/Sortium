import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Set, Generator, Sequence


class FileUtils:
    """
    FileUtils class for file utilities that provides various methods for working with files and directories and also are used in the Sorter class.
    A Custom FileUtils class can be provided to the Sorter class to satisfy the specific requirements.
    """

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
        path: Path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        return datetime.fromtimestamp(path.stat().st_mtime)

    def iter_files_and_sub_dirs(
        self, folder_path: str, ignore_dir: Sequence[str] | None = None
    ) -> tuple[Generator[str, None, None], Generator[str, None, None]]:
        """
        Yields two generators: one for subdirectories and one for files in a given folder.

        Args:
            folder_path (str): Path to the folder to iterate.
            ignore_dir (List[str] | None, optional): Names of subdirectories to ignore.

        Yields:
            tuple[Generator[str, None, None], Generator[str, None, None]]:
                A tuple containing two generators. The first one yields subdirectories
                and the second one yields files.
        """
        source_root = Path(folder_path)
        ignore_set = set(ignore_dir or [])

        def splitter() -> Generator[tuple[str, str], None, None]:
            for item in source_root.iterdir():
                if item.name in ignore_set:
                    continue
                if item.is_symlink():
                    continue
                if item.is_dir():
                    yield "dir", item.name
                elif item.is_file():
                    yield "file", item.name

        def subdirs():
            for kind, name in splitter():
                if kind == "dir":
                    yield name

        def files():
            for kind, name in splitter():
                if kind == "file":
                    yield name

        return subdirs(), files()

    def flatten_dir(
        self,
        folder_path: str,
        dest_folder_path: str,
        ignore_dir: Sequence[str] | None = None,
        rm_subdir: bool = False,
    ) -> None:
        """
        Moves all files from subdirectories of a given folder into a destination folder.

        This is useful for flattening a directory structure by collecting all files
        from nested folders and moving them into one target folder.

        Args:
            folder_path (str): Path to the root folder containing subdirectories with files.
            dest_folder_path (str): Path to the folder where all files should be moved.
            ignore_dir (List[str]): Names of subdirectories within `folder_path` that should be ignored during processing.
            rm_subdir (bool): If True, subdirectories will be removed after moving their contents. Default is False.
        Raises:
            FileNotFoundError: If the root folder (`folder_path`) does not exist.

        Notes:

            - Any errors encountered while moving files or removing subdirectories are caught and printed, but not raised.
            - Fails silently (with printed messages) on permission issues, missing files, or non-empty directories.
        """
        source_root: Path = Path(folder_path)
        dest_root: Path = Path(dest_folder_path)
        if not source_root.exists():
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

        dest_root.mkdir(parents=True, exist_ok=True)
        ignore_set = set(ignore_dir or [])

        try:
            # Get the list of files and sub directories.
            sub_dir_gen, file_gen = self.iter_files_and_sub_dirs(
                folder_path, ignore_dir
            )
            sub_dir_list = [d for d in sub_dir_gen if d not in ignore_set]
            file_list = list(file_gen)

            for name in file_list:
                source_item = source_root / name
                dest_item = dest_root / name
                try:
                    shutil.move(str(source_item), str(dest_item))
                except Exception as e:
                    print(f"Failed to move '{source_item}' to '{dest_item}': {e}")

            for sub_dir_name in sub_dir_list:
                self.flatten_dir(
                    str(source_root / sub_dir_name),
                    str(dest_root),
                    ignore_dir,
                    rm_subdir,
                )

            if rm_subdir:
                for sub_dir_name in sub_dir_list:
                    sub_dir_path = source_root / sub_dir_name
                    try:
                        if sub_dir_path != dest_root:
                            shutil.rmtree(sub_dir_path)
                    except Exception as e:
                        print(f"Failed to remove directory '{sub_dir_path}': {e}")
        except Exception as e:
            print(f"Error occurred while cleaning up folders: {e}")

    def find_unique_extensions(
        self, source_path: str, ignore_dir: List[str] | None = None
    ) -> Set[str]:
        """
        Recursively finds all unique file extensions in a given directory and its subdirectories.

        Args:
            source_path (str): Path to the root directory.
            ignore_dir (List[str], optional): List of directory names to ignore. Defaults to None.

        Returns:
            Set[str]: A set of unique file extensions found in the directory tree.

        Raises:
            FileNotFoundError: If the source_path does not exist.
        """
        source_root: Path = Path(source_path)
        if not source_root.exists():
            raise FileNotFoundError(
                f"The folder path '{str(source_root)}' does not exist."
            )

        extension_list: Set[str] = set()

        try:
            sub_dir_list, file_list = self.iter_files_and_sub_dirs(
                str(source_root), ignore_dir
            )

            for name in file_list:
                extension_list.add(Path(name).suffix.lower())

            for sub_dir_name in sub_dir_list:
                sub_dir_path = source_root / sub_dir_name
                extension_list.update(
                    self.find_unique_extensions(str(sub_dir_path), ignore_dir)
                )

        except Exception as e:
            print(f"Error occurred while finding unique extensions: {e}")

        return extension_list
