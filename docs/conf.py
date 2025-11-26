import os
import sys

from sortium import __version__ as sortium_version

# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "Sortium"
author = "Sarthak Goyal"
copyright = "2025, Sarthak Goyal"
version = ".".join(sortium_version.split(".")[:2])
release = sortium_version

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
html_logo = "_static/images/sortium-logo-full.png"
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "logo": {
        "image_light": "images/sortium-logo-full.png",
        "image_dark": "images/sortium-logo-full.png",
        "text": "Sortium",
    },
    "primary_sidebar_end": ["indices.html", "searchbox.html"],
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Sarthak-G0yal/Sortium",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/sortium/",
            "icon": "fa-solid fa-box",
        },
    ],
    "use_edit_page_button": False,
    "show_nav_level": 2,
}

html_css_files = [
    "styles/custom.css",
]
