PyGADM
======

.. toctree::
   :hidden:

   setup
   api <_api/modules>
   examples

Easy access to administrative boundary defined by GADM from Python scripts

install it using either ``pip`` or ``conda``: 

.. code-block:: console

   pip install pygadm 

and then request area of interest from their name or GADM Id: 

.. jupyter-execute:: 

   import pygadm 

   gdf = pygadm.get_items(name="Singapore", content_level=1)
   gdf.plot(cmap = "viridis")

