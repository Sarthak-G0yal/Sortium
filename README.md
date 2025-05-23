# 🗂️ SortPy

A Python utility to **automatically sort files** in a folder by their **type** (e.g., Images, Documents, Videos, etc.) and by their **last modified date**.

---

## 🚀 Features

- ✅ Sort files into folders by type (e.g., Images, Documents, Videos, Music, Others)
- 📅 Optionally sort files by last modified date within each type
- 📁 Optionally flatten subfolders

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Sarthak-G0yal/SortPy.git
cd SortPy

# Install in editable mode
pip install -e .
```

## 🧾 Usage

### 1. Import and Initialize

```python
from SortPy import Sorter

# Define file type categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".doc", ".pptx"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Music": [".mp3", ".wav", ".aac"],
    "Others": []
}

sorter = Sorter(file_types)
```

---

### 2. Sort Files by Type

```python
sorter.sort_by_type("/path/to/your/folder")
```

After execution, files will be moved into subfolders like `Images/`, `Documents/`, etc., based on their extensions.

---

### 3. Sort Files by Date

```python
sorter.sort_by_date("/path/to/your/folder", ["Images", "Documents", "Videos", "Music"])
```

Files inside each category will be sorted into folders by date (e.g., `06-May-2025/`).

---

### 4. Flatten Subdirectories (optional)

```python
sorter.move_it_out("/path/to/source", "/path/to/target")
```

Moves all files from subfolders into a single directory and deletes the empty subfolders.

---

## 🧪 Run Tests

```bash
pytest --cov=tests
```

---

## 👤 Author

**Sarthak Goyal**
📧 [sarthakgoyal487@gmail.com](mailto:sarthakgoyal487@gmail.com)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
