from pathlib import Path
from datetime import datetime
import shutil


def get_file_modified_date(file_path: str) -> datetime:
    """
    Returns the last modified datetime of a file.

    Args:
        file_path (str): Full path to the file.

    Returns:
        datetime: Datetime object representing the last modification time.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")
    return datetime.fromtimestamp(path.stat().st_mtime)


def get_subdirectories_names(
    folder_path: str, ignore_dir: list[str] = None
) -> list[str]:
    folder = Path(folder_path)
    if ignore_dir is None:
        ignore_dir = []
    sub_dir_list = [
        item.name
        for item in folder.iterdir()
        if item.is_dir() and item.name not in ignore_dir
    ]
    return sub_dir_list


def flatten_dir(
    folder_path: str,
    dest_folder_path: str,
    ignore_dir: list[str] = None,
    rm_subdir: bool = False,
) -> None:
    """
    Moves all files from subdirectories of a given folder into a destination folder.

    This is useful for flattening a directory structure by collecting all files
    from nested folders and moving them into one target folder.

    Args:
        folder_path (str): Path to the root folder containing subdirectories with files.
        dest_folder_path (str): Path to the folder where all files should be moved.
        ignore_dir (list[str]): Names of subdirectories within `folder_path` that should be ignored during processing.
        rm_subdir (bool): If True, subdirectories will be removed after moving their contents.

    Raises:
        FileNotFoundError: If the root folder (`folder_path`) does not exist.

    Notes:

        - Any errors encountered while moving files or removing subdirectories are
          caught and printed, but not raised.
        - Fails silently (with printed messages) on permission issues, missing files, or non-empty directories during deletion.
    """

    source_root = Path(folder_path)
    dest_root = Path(dest_folder_path)
    if not source_root.exists():
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    dest_root.mkdir(parents=True, exist_ok=True)

    try:
        # Get name of the sub directories ignoring the one in ignore_dir list.
        sub_dir_list = get_subdirectories_names(str(source_root), ignore_dir)

        # Get the list of files to be moved.
        file_list = [
            item.name
            for item in source_root.iterdir()
            if item.is_file() and item.name not in (ignore_dir or [])
        ]

        # If file_list empty then then return the function for sub_dir.
        if sub_dir_list and not file_list:
            for sub_dir_name in sub_dir_list:
                flatten_dir(
                    str(source_root / sub_dir_name),
                    str(dest_root),
                    ignore_dir,
                )

        # Move the files in the file_list to the dest_folder and check for folder in sub_dir_list.
        elif file_list:
            for name in file_list:
                source_item = source_root / name
                dest_item = dest_root / name
                try:
                    shutil.move(str(source_item), str(dest_item))
                except Exception as e:
                    print(f"Failed to move '{source_item}' to '{dest_item}': {e}")
            if sub_dir_list:
                for sub_dir_name in sub_dir_list:
                    flatten_dir(
                        str(source_root / sub_dir_name),
                        str(dest_root),
                        ignore_dir,
                    )

                # Remove the sub directories if rm_subdir is True.
                if rm_subdir:
                    for sub_dir_name in sub_dir_list:
                        sub_dir_path = source_root / sub_dir_name
                        try:
                            shutil.rmtree(sub_dir_path)
                        except Exception as e:
                            print(f"Failed to remove directory '{sub_dir_path}': {e}")

    except Exception as e:
        print(f"Error occurred while cleaning up folders: {e}")
