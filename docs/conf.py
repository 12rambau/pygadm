"""Configuration file for the Sphinx documentation builder."""

import os

# -- Path setup ----------------------------------------------------------------
from datetime import datetime

package_path = os.path.abspath("../..")
os.environ["PYTHONPATH"] = ":".join((package_path, os.environ.get("PYTHONPATH", "")))


# -- Project information -------------------------------------------------------
project = "pyGADM"
author = "Pierrick Rambaud"
copyright = f"2024-{datetime.now().year}, {author}"
release = "0.5.2"

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_favicon",
    "jupyter_sphinx",
    "autoapi.extension",
]
templates_path = ["_template"]
exclude_patterns = ["**.ipynb_checkpoints"]  # when working in a Jupyter env.

# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autoclass_content = "class"
autodoc_typehints = "description"

# -- Options of the HTML theme -------------------------------------------------
html_theme_options = {
    "use_edit_page_button": True,
    "show_prev_next": True,
    "logo": {
        "text": project,
        "image_light": "logo.png",
        "image_dark": "logo.png",
    },
    "footer_end": ["theme-version", "pypackage-credit"],
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

favicons = [
    {
        "rel": "apple-touch-icon",
        "size": "180x180",
        "static-file": "apple-touch-icon.png",
    },
    {
        "rel": "icon",
        "type": "image/png",
        "size": "32x32",
        "static-file": "favicon-32x32.png",
    },
    {
        "rel": "icon",
        "type": "image/png",
        "size": "16x16",
        "static-file": "favicon-16x16.png",
    },
    {"rel": "mask-icon", "static-file": "safari-pinned-tab.svg", "color": "#186691"},
    {"rel": "manifest", "static-file": "/site.webmanifest"},
]

# -- Options for autosummary/autodoc output ------------------------------------
autodoc_typehints = "description"
autoapi_dirs = ["../pygadm"]
autoapi_python_class_content = "init"
autoapi_member_order = "groupwise"
autoapi_root = "api"

# -- Options for autosectionlabel ----------------------------------------------
autosectionlabel_prefix_document = True

# -- Options for intersphinx ---------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "geopandas": ("https://geopandas.org/", None),
}
