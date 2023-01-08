PyGADM
======

.. image:: https://img.shields.io/readthedocs/pygadm?logo=readthedocs&logoColor=white
    :target: https://pygadm.readthedocs.io/en/stable
    :alt: Documentation Status
    
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT

.. image:: https://img.shields.io/pypi/v/pygadm?logo=python&logoColor=white
   :target: https://pypi.org/project/pygadm/
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/pygadm?label=version&logo=python&logoColor=white
   :target: https://pypi.org/project/pygadm/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/github/actions/workflow/status/12rambau/pygadm/unit.yaml?logo=github&logoColor=white
   :target: https://github.com/12rambau/pygadm/actions/workflows/unit.yaml
   :alt: Build

.. image:: https://img.shields.io/codeclimate/maintainability/12rambau/pygadm?logo=codeclimate&logoColor=white
   :target: https://codeclimate.com/github/12rambau/pygadm/maintainability
   :alt: Maintainability

.. image:: https://img.shields.io/codecov/c/github/12rambau/pygadm?label=codecov&logo=codecov&logoColor=white&token=O6ksUUazr4
   :target: https://codecov.io/gh/12rambau/pygadm
   :alt: Coverage
    
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black badge
   
.. image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg
   :target: https://conventionalcommits.org
   :alt: conventional commit

Easy access to administrative boundary defined by GADM from a Python scripts.

Thi lib provides access to GADM datasets from a Python script without downloading the file from their server. We provide access to The current version (4.1.) which delimits 400,276 administrative areas. 

The data are freely available for academic use and other non-commercial use. Redistribution, or commercial use is not allowed without prior permission. See the `license <https://gadm.org/license.html>`__ of the GADM project for more details.

.. note:: 

   the dataset are generated in the GADM (Global Administrative Areas) project from Berkeley University. Any request relative to the geometries should be redirected to them. 

install it using either ``pip`` or ``conda``: 

.. code-block:: console

   pip install pygadm 

and then request area of interest from their name or GADM Id: 

.. code-block:: python

   import pygadm 

   gdf = pygadm.get_items(name="Singapore", content_level=1)
