Sortium Documentation
=====================

Welcome to **Sortium**, a Python utility for organizing files by type, modification date, and custom patterns.

**Sortium** enables efficient file management by:

- Categorizing files into folders such as Images, Documents, Music, Videos, and Others

- Organizing files within each category based on their last modified date

- Flattening nested directory structures into a single-level hierarchy before sorting

- Supporting custom file organization using user-defined regular expression (regex) patterns

.. contents::
   :local:
   :depth: 1

Quick Start
-----------

.. warning::

   **Always make a backup of your files before running Sortium.**
   This utility moves files and modifies folder structures, which may lead to data loss if misused.

Install via pip:

.. code-block:: console

   pip install sortium

Then:

.. code-block:: python

   from sortium import Sorter

   sorter = Sorter()

   # Sort files by type into categorized folders
   sorter.sort_by_type("/path/to/folder")

   # Further sort files inside specific category folders by their last modified date
   sorter.sort_by_date("/path/to/folder", ["Images", "Documents"])

   # Sort files using custom regex patterns
   regex_patterns = {
       "Reports": r"^report_.*\.pdf$",
       "Logs": r".*\.log$"
   }
   sorter.sort_by_regex("/path/to/source", regex_patterns, "/path/to/destination")


API Reference
-------------

.. toctree::
   :maxdepth: 2

   modules

Project Info
------------

- **Repository**: `GitHub – Sortium <https://github.com/Sarthak-G0yal/Sortium>`_
- **License**: GNU v3.0
- **Author**: Sarthak Goyal
