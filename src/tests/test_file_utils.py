import os
import pytest
from pathlib import Path
from sortium.file_utils import FileUtils
from .test_file_tree import setup_test_dirs

file_utiles = FileUtils()


def test_flatten_dir_moves_files(setup_test_dirs):
    file_utiles.flatten_dir(setup_test_dirs["base"], setup_test_dirs["dest"])

    dest_files = os.listdir(setup_test_dirs["dest"])
    expected_files = [Path(f).name for f in setup_test_dirs["files"]]

    for file in expected_files:
        assert file in dest_files

    # Ignored file should be moved in this test
    assert Path(setup_test_dirs["ignored_file"]).name in dest_files


def test_flatten_dir_moves_files_ignored(setup_test_dirs):
    ignored_name = setup_test_dirs["ignored"].name

    file_utiles.flatten_dir(
        setup_test_dirs["base"], setup_test_dirs["dest_test"], ignore_dir=[ignored_name]
    )

    dest_files = os.listdir(setup_test_dirs["dest_test"])
    expected_files = [Path(f).name for f in setup_test_dirs["files"]]

    for file in expected_files:
        assert file in dest_files

    # Ensure ignored file is not moved
    assert Path(setup_test_dirs["ignored_file"]).name not in dest_files
    assert os.path.exists(setup_test_dirs["dest_test"])


def test_flatten_dir_moves_files_source_error(setup_test_dirs):
    with pytest.raises(FileNotFoundError):
        file_utiles.flatten_dir(
            "wrong_path",
            setup_test_dirs["dest"],
            ignore_dir=[setup_test_dirs["ignored"].name],
        )


def test_flatten_dir_remove_subdir(setup_test_dirs):
    file_utiles.flatten_dir(
        setup_test_dirs["base"], setup_test_dirs["dest"], rm_subdir=True
    )
    assert not setup_test_dirs["sub1"].exists()
    assert not setup_test_dirs["sub_sub1"].exists()


def test_find_unique_extensions(setup_test_dirs):
    unique_extensions = file_utiles.find_unique_extensions(setup_test_dirs["base"])
    for ext in setup_test_dirs["unique_extensions"]:
        assert ext in unique_extensions


def test_find_unique_extensions_error():
    with pytest.raises(FileNotFoundError):
        file_utiles.find_unique_extensions("invalid/path")
