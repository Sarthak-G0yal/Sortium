Sortium Documentation
=====================

Welcome to **Sortium**, a Python utility for organizing files by type and modification date.

Sortium helps you:

- Automatically sort files into categories (Images, Documents, Music, etc.)
- Organize files within categories by their last modified date
- Flatten deeply nested folder structures

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
   sorter.sort_by_type("/path/to/folder")
   sorter.sort_by_date("/path/to/folder", ["Images", "Documents"])

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Sortium Package

   modules

Project Info
------------

- **Repository**: `GitHub – Sortium <https://github.com/Sarthak-G0yal/Sortium>`_
- **License**: GNU v3.0
- **Author**: Sarthak Goyal
