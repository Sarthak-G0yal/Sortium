import os
import shutil
import tempfile
import pytest
from datetime import datetime
from SortPy import flatten_the_dir, get_file_modified_date, get_subdirectories_names


def create_temp_file(directory, name, content="test"):
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write(content)
    return path


@pytest.fixture
def setup_test_dirs():
    base = tempfile.mkdtemp()
    dest = os.path.join(base, "flattened")
    os.mkdir(dest)

    sub1 = os.path.join(base, "sub1")
    sub2 = os.path.join(base, "sub2")
    os.mkdir(sub1)
    os.mkdir(sub2)

    # Ignored dir
    ignored = os.path.join(base, "ignoreme")
    os.mkdir(ignored)

    file1 = create_temp_file(sub1, "file1.txt", "data1")
    file2 = create_temp_file(sub2, "file2.txt", "data2")
    ignored_file = create_temp_file(ignored, "ignored.txt", "ignored")

    yield {
        "base": base,
        "dest": dest,
        "files": [file1, file2],
        "ignored": ignored,
        "ignored_file": ignored_file,
    }

    shutil.rmtree(base)


def test_get_file_modified_date(setup_test_dirs):
    file_path = setup_test_dirs["files"][0]
    modified_time = get_file_modified_date(file_path)
    assert isinstance(modified_time, datetime)


def test_get_subdirectories_names(setup_test_dirs):
    base = setup_test_dirs["base"]
    ignore = [os.path.basename(setup_test_dirs["ignored"])]
    subdirs = get_subdirectories_names(base, ignore_dir=ignore)
    assert "sub1" in subdirs
    assert "sub2" in subdirs
    assert "ignoreme" not in subdirs


def test_flatten_the_dir_moves_files(setup_test_dirs):
    flatten_the_dir(
        setup_test_dirs["base"], setup_test_dirs["dest"], ignore_dir=["ignoreme"]
    )

    dest_files = os.listdir(setup_test_dirs["dest"])
    assert "file1.txt" in dest_files
    assert "file2.txt" in dest_files

    # Ignored file should still exist
    assert os.path.exists(setup_test_dirs["ignored_file"])


def test_flatten_the_dir_removes_subdirs(setup_test_dirs):
    flatten_the_dir(
        setup_test_dirs["base"], setup_test_dirs["dest"], ignore_dir=["ignoreme"]
    )

    assert not os.path.exists(os.path.join(setup_test_dirs["base"], "sub1"))
    assert not os.path.exists(os.path.join(setup_test_dirs["base"], "sub2"))
    assert os.path.exists(setup_test_dirs["ignored"])  # ignored dir should remain
