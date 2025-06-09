import os
import sys

# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "Sortium"
author = "Sarthak Goyal"
copyright = "2025, Sarthak Goyal"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Add the path to your source code
sys.path.insert(0, os.path.abspath("../src"))

# -- Options for Napoleon ----------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

