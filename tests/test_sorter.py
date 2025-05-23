from SortPy import Sorter

# Define categories
file_types : dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".doc", ".pptx"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    "Others": [],
}


def test_get_category_images() -> None:
    sorter = Sorter(file_types)
    ext = ".jpg"
    type = sorter.get_category(ext)
    assert type == "Images"


def test_get_category_others() -> None:
    sorter = Sorter(file_types)
    ext = ".m"
    type = sorter.get_category(ext)
    assert type == "Others"
