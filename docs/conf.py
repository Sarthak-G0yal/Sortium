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

html_static_path = ["_static"]
html_favicon = "_static/images/sortium-favicon.ico"
html_theme = "furo"

html_theme_options = {
    "light_logo": "images/sortium-logo-light.png",
    "dark_logo": "images/sortium-logo.png",
    "dark_css_variables": {
        "color-foreground-primary": "#fdfdfd",
        "color-background-primary": "#0e1116",
        "color-brand-primary": "#f9aa1f",
        "color-brand-content": "#f25c2e",
        "color-sidebar-background": "#0e1116",
        "color-sidebar-link-text": "#fdfdfd",
        "color-sidebar-link-text--top-level": "#f9aa1f",
        "color-sidebar-link-text--active": "#f25c2e",
    },
}

