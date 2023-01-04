Installation
============

Stable release 
--------------

install it using either ``pip`` or ``conda``:

.. tab-set::

   .. tab-item:: pip

      .. code-block:: console
   
         pip install pygadm

   .. tab-item:: conda

      .. code-block:: console

         conda install pygadm

From source
-----------

The source of ``pygadm`` can be installed from the `GitHub repo <https://github.com/12rambau/pygadm>`_:

.. code-block:: console

   python -m pip install git+git://github.com/12rambau/pygadm.git#egg=pygadm 
   
local development
-----------------

For local development, don't forget to install the pre-commit hooks before making changes. These hooks are tested in the CI.

.. code-block:: console

   git clone https://github.com/12rambau/pygadm.git
   cd pygadm/
   pre-commit install -t pre-commit -t commit-msg
   pip install -e .
