PyGADM
======

.. toctree::
   :hidden:

   setup
   usage
   API <_api/modules>

Easy access to administrative boundary defined by GADM from a Python scripts.

Thi lib provides access to GADM datasets from a Python script without downloading the file from their server. We provide access to The current version (4.1.) which delimits 400,276 administrative areas. 

The data are freely available for academic use and other non-commercial use. Redistribution, or commercial use is not allowed without prior permission. See the `license <https://gadm.org/license.html>`__ of the GADM project for more details.

.. note:: 

   the dataset are generated in the GADM (Global Administrative Areas) project from Berkeley University. Any request relative to the geometries should be redirected to them. 

.. grid:: 1 2 2 3
    :gutter: 2

    .. grid-item-card:: :fas:`download` Installation
        :link: setup.html

        Learn how to install the lib from differnet sources

    .. grid-item-card:: :fas:`book-open` Usage
        :link: usage.html

        Usage demonstration of the lib

    .. grid-item-card:: :fas:`plug` API references
        :link: _api/module.html

        the complete API reference

install it using either ``pip`` or ``conda``: 

.. code-block:: console

   pip install pygadm 

and then request area of interest from their name or GADM Id: 

.. code-block:: 

   import pygadm 

   gdf = pygadm.get_items(name="Singapore", content_level=1)

