PyGADM
======

.. toctree::
   :hidden:

   setup
   usage
   API <_api/modules>

Easy access to administrative boundary defined by GADM from Python scripts

install it using either ``pip`` or ``conda``: 

.. code-block:: console

   pip install pygadm 

and then request area of interest from their name or GADM Id: 

.. code-block:: 

   import pygadm 

   gdf = pygadm.get_items(name="Singapore", content_level=1)

