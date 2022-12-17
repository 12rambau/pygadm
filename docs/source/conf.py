"""
Configuration file for the Sphinx documentation builder.
"""

# import os
# import sys

# -- Path setup ----------------------------------------------------------------
from datetime import datetime

from pygadm import __author__, __version__  # noqa

# sys.path.insert(0, os.path.abspath("."))
# sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -------------------------------------------------------

project = "pygadm"
copyright = f"2022-{datetime.now().year}, {__author__}"
author = __author__
release = __version__

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "nbsphinx",
    "sphinx_copybutton",
    # https://github.com/spatialaudio/nbsphinx/issues/687
    "IPython.sphinxext.ipython_console_highlighting",
    "jupyter_sphinx",
]
templates_path = ["_templates"]
exclude_patterns = ["**.ipynb_checkpoints"]  # when working in a Jupyter env.

# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autoclass_content = "class"

# -- Options of the HTML theme -------------------------------------------------
html_theme_options = {
    "use_edit_page_button": True,
    "show_prev_next": False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/12rambau/pygadm",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Pypi",
            "url": "https://pypi.org",
            "icon": "fa-brands fa-python",
        },
    ],
}
html_context = {
    "github_user": "12rambau",
    "github_repo": "pygadm",
    "github_version": "main",
    "doc_path": "docs/source",
}
