.. sorter documentation master file, created by
   sphinx-quickstart on Sat Jan 01 00:00:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#######################################
Welcome to Sortium's Documentation
#######################################

.. raw:: html

    <section class="sortium-hero">
       <div class="sortium-hero__content">
          <p class="hero-eyebrow">Plan-first file orchestration</p>
          <h1>Preview every move before touching disk.</h1>
          <p>Sortium scans millions of files without blowing up memory, builds human-readable JSON plans, and applies them only when you are ready. Audit, edit, or hand off the plan with confidence.</p>
          <div class="sortium-hero__actions">
             <a class="sortium-btn primary" href="https://pypi.org/project/sortium/">pip install sortium</a>
             <a class="sortium-btn ghost" href="https://github.com/Sarthak-G0yal/Sortium">View on GitHub</a>
          </div>
       </div>
       <div class="sortium-hero__stats">
          <div class="sortium-stat-card">
             <span>JSON</span>
             Plan files you can diff and version.
          </div>
          <div class="sortium-stat-card">
             <span>3+</span>
             Sorting modes: type, date, regex.
          </div>
          <div class="sortium-stat-card">
             <span>0</span>
             Overwrites thanks to collision guards.
          </div>
       </div>
    </section>

.. raw:: html

    <section class="sortium-feature-grid">
       <article class="sortium-feature">
          <h3>Plan-First Workflow</h3>
          <p>Generate editable JSON instructions and keep them under git to document every move.</p>
       </article>
       <article class="sortium-feature">
          <h3>Flexible Categorization</h3>
          <p>Mix file-type buckets, date partitions, and regex captures to shape exactly how archives look.</p>
       </article>
       <article class="sortium-feature">
          <h3>Safety Nets Built-In</h3>
          <p>Automatic collision avoidance, dry-run previews, and deterministic destination builders.</p>
       </article>
       <article class="sortium-feature">
          <h3>Minimal Memory Footprint</h3>
          <p>Streams directories with generators so even sprawling NAS shares stay manageable.</p>
       </article>
       <article class="sortium-feature">
          <h3>Recursive On-Demand</h3>
          <p>Flip a ``recursive=True`` flag on any strategy to pull nested files into the plan—or leave it off for shallow sweeps.</p>
       </article>
    </section>

.. note::

    This documentation covers installation, usage guides, and the complete API reference for Sortium.

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
   plan_path = sorter.sort_by_type(my_folder, recursive=True)

   # Inspect/edit the JSON if desired, then apply it
   sorter.file_utils.apply_move_plan(str(plan_path))

.. tip::

   Drop ``recursive=True`` (the default) if you only want to move files living directly inside ``my_folder``.


**Example 2: Sorting to a New Destination**

Organize files from a source folder and move the categorized results to a separate, clean location.

.. code-block:: python

   from sortium.sorter import Sorter

   source_dir = "/path/to/source_files"
   destination_dir = "/path/to/organized_archive"

   sorter = Sorter()

   # Prepare a plan that moves files into categorized folders inside destination_dir
   plan_path = sorter.sort_by_type(
      source_dir,
      dest_folder_path=destination_dir,
      recursive=True,
   )
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
   plan_path = sorter.sort_by_regex(
      project_folder,
      regex_patterns,
      sorted_output,
      recursive=True,
   )
   sorter.file_utils.apply_move_plan(str(plan_path))

.. note::

   ``recursive`` defaults to ``True`` for regex sorting so deep project trees are handled automatically. Pass ``recursive=False`` to limit the scan to the root directory only.


Project Info
------------

- **Repository**: `GitHub – Sortium <https://github.com/Sarthak-G0yal/Sortium>`_
- **PyPI Project**: `Sortium on PyPI <https://pypi.org/project/sortium/>`_
- **License**: GNU General Public License v3.0
- **Author**: Sarthak Goyal