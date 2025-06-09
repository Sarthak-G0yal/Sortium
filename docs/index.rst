Sortium Documentation
=====================

Welcome to the documentation for **Sortium**, a Python utility for organizing files by type and modification date.

Sortium helps you:

- Automatically sort files into categories (e.g., Images, Documents, Music)
- Organize files within categories by their last modified date
- Flatten deeply nested folder structures

This documentation provides an overview of the library, its modules, and usage examples.

.. contents::
   :local:
   :depth: 1

Get Started
-----------

Sortium can be used via the main ``Sorter`` class or utility functions:

.. code-block:: python

   from sortium import Sorter

   sorter = Sorter()
   sorter.sort_by_type("/path/to/folder")
   sorter.sort_by_date("/path/to/folder", ["Images", "Documents"])

Modules
-------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   modules

Project Info
------------

- Repository: https://github.com/Sarthak-G0yal/Sortium
- License: MIT
- Author: Sarthak Goyal

