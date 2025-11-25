.. sorter documentation master file, created by
   sphinx-quickstart on Sat Jan 01 00:00:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#######################################
Welcome to Sortium's Documentation
#######################################

**Sortium** is a high-performance Python utility designed for rapidly organizing file systems. It emphasizes a plan-first workflow so you can preview, edit, and even reverse categorized moves (by type, date, or regex) before they touch disk.

Designed for both speed and safety, it is memory-efficient for handling massive directories and automatically prevents file overwrites.

Core Features
-------------

*   **Plan-First Workflow**: Generates editable JSON move plans so you can audit, tweak, or hand off the intended operations before applying them.

*   **Versatile Sorting Logic**:
    *   **By Type**: Organize files into categories like ``Images``, ``Documents``, ``Archives``, etc.
    *   **By Date**: Further organize categorized files into date-stamped folders (e.g., ``01-Jan-2023``).
    *   **By Regex**: Use powerful, custom regex patterns to categorize files recursively.

*   **Safe and Controlled Operations**:
    *   Automatically handles file name collisions to prevent accidental data loss.
    *   Sort files in-place or move them to a completely separate destination directory.

*   **Memory-Efficient Design**: Employs generators to process files one by one, ensuring a tiny memory footprint even with millions of files.


.. note::

   This documentation provides installation instructions, usage examples, and the complete API reference for the Sortium library.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


A 30-Second Guide
-----------------

.. warning::

   **Always back up your files before running Sortium.**
   This utility performs file move operations that modify your directory structure. Misuse could lead to data loss.

First, install the library via pip:

.. code-block:: console

   pip install sortium


**Example 1: Basic Sorting by Type (In-Place)**

This is the simplest use case. It organizes all files in a folder into subdirectories like ``Images``, ``Documents``, and ``Videos``.

.. code-block:: python

   from sortium.sorter import Sorter

   # The folder you want to clean up
   my_folder = "/path/to/my_messy_downloads"

   # Create a Sorter instance and produce a plan
   sorter = Sorter()
   plan_path = sorter.sort_by_type(my_folder)

   # Inspect/edit the JSON if desired, then apply it
   sorter.file_utils.apply_move_plan(str(plan_path))


**Example 2: Sorting to a New Destination**

Organize files from a source folder and move the categorized results to a separate, clean location.

.. code-block:: python

   from sortium.sorter import Sorter

   source_dir = "/path/to/source_files"
   destination_dir = "/path/to/organized_archive"

   sorter = Sorter()

   # Prepare a plan that moves files into categorized folders inside destination_dir
   plan_path = sorter.sort_by_type(source_dir, dest_folder_path=destination_dir)
   sorter.file_utils.apply_move_plan(str(plan_path))


**Example 3: Advanced Sorting with Regex**

Recursively scan a directory and sort files based on custom patterns. This is great for organizing project files, logs, or datasets.

.. code-block:: python

   from sortium.sorter import Sorter

   project_folder = "/path/to/data_science_project"
   sorted_output = "/path/to/sorted_project_files"

      # Define categories and their corresponding regex patterns
      regex_patterns = {
         "Datasets": r".*\.csv$",
         "Notebooks": r".*\.ipynb$",
         "Final_Reports": r"final_report_.*\.pdf$"
      }

      sorter = Sorter()
      plan_path = sorter.sort_by_regex(project_folder, regex_patterns, sorted_output)
      sorter.file_utils.apply_move_plan(str(plan_path))


Project Info
------------

- **Repository**: `GitHub – Sortium <https://github.com/Sarthak-G0yal/Sortium>`_
- **PyPI Project**: `Sortium on PyPI <https://pypi.org/project/sortium/>`_
- **License**: GNU General Public License v3.0
- **Author**: Sarthak Goyal