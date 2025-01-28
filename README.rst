PyGADM
======

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg?logo=opensourceinitiative&logoColor=white
    :target: LICENSE
    :alt: License: MIT

.. |commit| image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?logo=git&logoColor=white
   :target: https://conventionalcommits.org
   :alt: conventional commit

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: ruff badge

.. |prettier| image:: https://img.shields.io/badge/code_style-prettier-ff69b4.svg?logo=prettier&logoColor=white
   :target: https://github.com/prettier/prettier
   :alt: prettier badge

.. |pre-commmit| image:: https://img.shields.io/badge/pre--commit-active-yellow?logo=pre-commit&logoColor=white
    :target: https://pre-commit.com/
    :alt: pre-commit

.. |pypi| image:: https://img.shields.io/pypi/v/pygadm?color=blue&logo=pypi&logoColor=white
    :target: https://pypi.org/project/pygadm/
    :alt: PyPI version

.. |conda| image:: https://img.shields.io/conda/vn/conda-forge/pygadm?color=blue&logo=anaconda&logoColor=white
    :target: https://anaconda.org/conda-forge/pygadm
    :alt: Conda Version

.. |build| image:: https://img.shields.io/github/actions/workflow/status/12rambau/pygadm/unit.yaml?logo=github&logoColor=white
    :target: https://github.com/12rambau/pygadm/actions/workflows/unit.yaml
    :alt: build

.. |coverage| image:: https://img.shields.io/codecov/c/github/12rambau/pygadm?logo=codecov&logoColor=white
    :target: https://codecov.io/gh/12rambau/pygadm
    :alt: Test Coverage

.. |docs| image:: https://img.shields.io/readthedocs/pygadm?logo=readthedocs&logoColor=white
    :target: https://pygadm.readthedocs.io/en/latest/
    :alt: Documentation Status

|license| |commit| |ruff| |prettier| |pre-commmit| |pypi| |conda| |build| |coverage| |docs|

Overview
--------

.. image:: docs/_static/logo.svg
    :width: 20%
    :align: right

Easy access to administrative boundary defined by GADM from a Python scripts.

This lib provides access to GADM datasets from a Python script without downloading the file from their server. We provide access to The current version (4.1.) which delimits 400,276 administrative areas.

The data are freely available for academic use and other non-commercial use. Redistribution, or commercial use is not allowed without prior permission. See the `license <https://gadm.org/license.html>`__ of the GADM project for more details.

.. note::

   the dataset are generated in the GADM (Global Administrative Areas) project from Berkeley University. Any request relative to the geometries should be redirected to them.

install it using either ``pip`` or ``conda``:

.. code-block:: console

   pip install pygadm

and then request area of interest from their name or GADM Id:

.. code-block:: python

   import pygadm

   gdf = pygadm.Items(name="Singapore", content_level=1)

Credits
-------

This package was created with `Copier <https://copier.readthedocs.io/en/latest/>`__ and the `@12rambau/pypackage <https://github.com/12rambau/pypackage>`__ 0.1.16 project template.
