import os
import sys

# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "SortPy"
author = "Sarthak Goyal"
copyright = "2025, Sarthak Goyal"
release = "1.0.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",  # adds links to source code
    "sphinx.ext.autosummary",  # for summary tables
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Add the path to your source code
sys.path.insert(
    0, os.path.abspath("../src/*")
)  # Adjusted to point to the SortPy package

# -- Options for Napoleon ----------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"  # Read the Docs theme
html_static_path = ["_static"]
