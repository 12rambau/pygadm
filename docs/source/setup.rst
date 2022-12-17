Installation
============

Stable release 
--------------

Use pip to install from `Pypi <https://pypi.org/project/pygadm/>`_:

.. code-block:: console
   
   pip install pygadm

From source
-----------

The source of ``pygadm`` can be installed from the `GitHub repo <https://github.com/12rambau/pygadm>`_:

.. code-block:: console

   python -m pip install git+git://github.com/12rambau/pygadm.git#egg=pygadm 
   
local development
-----------------

.. code-block:: console

   git clone https://github.com/12rambau/pygadm.git
   cd pygadm/
   pre-commit install -t pre-commit -t commit-msg
   pip install -e .