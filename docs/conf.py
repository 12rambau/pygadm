"""Configuration file for the Sphinx documentation builder."""

import os
import re

# -- Path setup ----------------------------------------------------------------
from datetime import datetime
from pathlib import Path

import ee
import httplib2

from pygadm import __author__, __version__

package_path = os.path.abspath("../..")
os.environ["PYTHONPATH"] = ":".join((package_path, os.environ.get("PYTHONPATH", "")))


# -- Project information -------------------------------------------------------

project = "PyGADM"
copyright = f"2022-{datetime.now().year}, {__author__}"
author = __author__
release = __version__

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_favicon",
    "jupyter_sphinx",
    "autoapi.extension",
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

# -- Script to authenticate to Earthengine using a token -----------------------
def gee_configure() -> None:
    """Initialize earth engine according to the environment.

    It will use the creddential file if the EARTHENGINE_TOKEN env variable exist.
    Otherwise it use the simple Initialize command (asking the user to register if necessary).
    """
    # only do the initialization if the credential are missing
    if not ee.data._credentials:

        # if the credentials token is asved in the environment use it
        if "EARTHENGINE_TOKEN" in os.environ:

            # get the token from environment variable
            ee_token = os.environ["EARTHENGINE_TOKEN"]

            # as long as RDT quote the token, we need to remove the quotes before writing
            # the string to the file
            pattern = r"^'[^']*'$"
            if re.match(pattern, ee_token) is not None:
                ee_token = ee_token[1:-1]

            # write the token to the appropriate folder
            credential_folder_path = Path.home() / ".config" / "earthengine"
            credential_folder_path.mkdir(parents=True, exist_ok=True)
            credential_file_path = credential_folder_path / "credentials"
            credential_file_path.write_text(ee_token)

        # if the user is in local development the authentication should
        # already be available
        ee.Initialize(http_transport=httplib2.Http())


gee_configure()
