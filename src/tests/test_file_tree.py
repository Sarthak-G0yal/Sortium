import pytest
from pathlib import Path
from typing import Generator, Dict
import os
import tempfile
import shutil


def create_temp_file(directory: str, name: str, content: str = "test") -> str:
    path = Path(directory) / name
    path.write_text(content)
    return path.name


@pytest.fixture
def setup_test_dirs() -> Generator[Dict[str, object], None, None]:
    base = Path(tempfile.mkdtemp())
    dest = Path(tempfile.mkdtemp())

    sub1 = base / "sub1"
    sub2 = base / "sub2"
    sub1.mkdir()
    sub2.mkdir()

    sub_sub1 = sub1 / "sub_sub1"
    sub_sub2 = sub2 / "sub_sub2"
    sub_sub1.mkdir()
    sub_sub2.mkdir()

    dest_test = dest / "dest_test"
    ignored = base / "ignoreme"
    ignored.mkdir()

    file_mp4 = create_temp_file(str(sub1), "video1.mp4", "video binary")
    file_outer = create_temp_file(str(sub1), "file_outer.txt", "outer_file")
    file_mp3 = create_temp_file(str(sub2), "audio1.mp3", "audio binary")
    file1 = create_temp_file(str(sub_sub1), "file1.txt", "data1")
    file_jpg = create_temp_file(str(sub_sub1), "image1.jpg", "fake image data")
    file2 = create_temp_file(str(sub_sub2), "file2.txt", "data2")
    file_html = create_temp_file(str(sub_sub2), "page1.html", "<html></html>")
    ignored_file = create_temp_file(str(ignored), "ignored.txt", "ignored")

    extra_files = [file_jpg, file_html, file_mp4, file_mp3]
    unique_extensions = [".jpg", ".html", ".mp4", ".mp3", ".txt"]

    yield {
        "base": base,
        "dest": dest,
        "dest_test": dest_test,
        "sub1": sub1,
        "sub_sub1": sub_sub1,
        "files": [file1, file2, file_outer, *extra_files],
        "ignored": ignored,
        "ignored_file": ignored_file,
        "unique_extensions": unique_extensions,
    }

    shutil.rmtree(base, ignore_errors=True)
    shutil.rmtree(dest, ignore_errors=True)
    shutil.rmtree(dest_test, ignore_errors=True)


@pytest.fixture
def setup_type_sort() -> Generator[Dict[str, object], None, None]:
    base = tempfile.mkdtemp()
    txt = create_temp_file(base, "doc.txt")
    jpg = create_temp_file(base, "image.jpg")
    mp3 = create_temp_file(base, "music.mp3")
    unknown = create_temp_file(base, "random.xyz")

    yield {
        "base": base,
        "files": [txt, jpg, mp3, unknown],
    }

    shutil.rmtree(base, ignore_errors=True)


@pytest.fixture
def setup_date_sort() -> Generator[Dict[str, object], None, None]:
    base = tempfile.mkdtemp()
    images_dir = os.path.join(base, "Images")
    docs_dir = os.path.join(base, "Documents")
    os.makedirs(images_dir)
    os.makedirs(docs_dir)

    file1 = create_temp_file(images_dir, "photo.png")
    file2 = create_temp_file(docs_dir, "report.pdf")

    yield {
        "base": base,
        "Images": images_dir,
        "Documents": docs_dir,
        "files": [file1, file2],
    }

    shutil.rmtree(base, ignore_errors=True)


@pytest.fixture
def setup_regex_tree() -> Generator[Dict[str, object], None, None]:
    base = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()

    type_1 = [
        "invoice_2025_july.pdf",
        "user_data_backup_2023_12.sql",
        "log_file_2025_07_01.txt",
    ]
    type_2 = ["Report2025Q2.pdf", "InvoiceJuly2025.docx", "BackupData2023Final.zip"]
    type_3 = ["img_12345.png", "user_987654.json", "order_20250701.csv"]

    re_patterns = {
        "type_1": r"^([a-z]+_)+\d{4}(_[a-z0-9]+)+\.[a-z]+$",
        "type_2": r"^[A-Z][a-zA-Z]+(20\d{2})(Q[1-4]|[A-Z][a-z]+)?[A-Za-z]*\.[a-z]+$",
        "type_3": r"^(img|user|order)_\d+\.[a-z]+$",
    }

    for file in type_1 + type_2 + type_3:
        create_temp_file(base, file)

    yield {
        "base": base,
        "dest": dest,
        "files_types": {
            "type_1": type_1,
            "type_2": type_2,
            "type_3": type_3,
        },
        "re_patterns": re_patterns,
    }

    shutil.rmtree(base, ignore_errors=True)
    shutil.rmtree(dest, ignore_errors=True)
