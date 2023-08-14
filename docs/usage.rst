Usage
=====

Get items
---------

The PyGADM lib can be used to extract information from the GADM dataset as GeoPandas :code:`GeoDataFrame`.

Countries
^^^^^^^^^

Using the :code:`get_items` methods, you can access an administrative area using either its name or its GADM identification code.

For example to extract the France geometry you can use the following code:

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(name="France")

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery,  zoom=5, center=[46.21, 2.21])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

If you know the code of the area you try to use, you can use the GADM code instead of the name.

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(admin="FRA")

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery,  zoom=5, center=[46.21, 2.21])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

Smaller admin levels
^^^^^^^^^^^^^^^^^^^^

One is not bind to only request a country, any level can be accessed using both names and/or GADM code.

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(name="Corse-du-Sud")

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery, zoom=8, center=[41.86, 8.97])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

.. warning::

    The names of countries are all unique but not the smaller administrative layers. If you request a small area using name, make sure it's the one you are looking for before running your workflow. follow :ref:`usage:Duplication issue` for more information.

Content of an admin layer
^^^^^^^^^^^^^^^^^^^^^^^^^

Using the :code:`content_level` option, one can require smaller administrative layer than the one setup in the name. For example when you request France, by setting up the :code:`content_level` option to 2, the geodataframe will include all the department geometries.

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(admin="FRA", content_level=2)

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery,  zoom=5, center=[46.21, 2.21])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

Request multiple areas at once
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 0.2.0

    names and admin can now be set as list

To perform regional analysis that aggregate multiple boundaries, you can now request them at once using a list of ``name`` or a list of ``admin``. In this example we request both germany and France at once:

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(name=["France", "Germany"])

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery,  zoom=5, center=[48.83, 5.17])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

Continents
^^^^^^^^^^

It's possible to request all countries from one single continent using one of the following names:

-   North America
-   South America
-   Antartica
-   Europe
-   Asia
-   Oceania
-   Africa

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(name="south america")

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery,  zoom=5, center=[-20.30, -59.32])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

.. note::

    it will load all the countries included in the continent. Using it requires a good internet conexion and a powerful computer to handle the produced ``geoDataFrame``. It is suggested to use it without smaller administrative areas.

Find names
----------

To get the available name and GADM code in a administrative layer you can use the :code:`get_names` method with the same parameters. Use then these names in a :code:`get_items` request to get the geometry.

For example to get the name and codes of all the departments in France you can run:

.. jupyter-execute::

    import pygadm

    pygadm.get_names(admin="FRA", content_level=2)

Google Earth engine
-------------------

.. note::

    We don't display the results of these cells because the GEE authentication is not working in RDT.

Transform gdf into ``ee.FeatureCollection``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use this lib with GEE, install the "earthengine-api" package in your environment and then run the following code and transform the ``GeoDataFrame`` into a ``ee.FeatureCollection`` as follow:

.. code-block:: python

    import pygadm
    import ee

    ee.Initialize()

    gdf = pygadm.get_items(name="Corse-du-Sud")

    # transform into an ee.FeatureCollection
    fc = ee.FeatureCollection(gdf.__geo_interface__)

Simplify geometry
^^^^^^^^^^^^^^^^^

The GADM dataset are describing the geometry of administrative areas in high-resolution. This may overload the authorized importation limits of earthengine which will lead to the following error:

.. code-block:: console

    EEException: Request payload size exceeds the limit: 10485760 bytes.

Use the :code:`simplify` method from GeoPandas (more information `here <https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.simplify.html>`__) to downscale the resolution of the geometries. The following example is needed if you want to work with France:

.. jupyter-execute::

    import pygadm
    import geemap
    import ee
    from ipyleaflet import ZoomControl

    ee.Initialize()

    gdf = pygadm.get_items(name="France")

    # reduce resolution
    gdf.geometry = gdf.geometry.simplify(tolerance=.001)

    # transform into an ee.FeatureCollection
    fc = ee.FeatureCollection(gdf.__geo_interface__)

    # in this example we use geemap to display the geometry on the map
    # the map is customized to have the same look & feel as the rest of the documentation
    m = geemap.Map(scroll_wheel_zoom=False, center=[46.21, 2.21], zoom=5, basemap="Esri.WorldImagery")
    m.clear_controls()
    m.add(ZoomControl())
    m.addLayer(fc, {"color": "red"}, "FRA")

    m

Duplication issue
-----------------

.. warning::

    The names of countries are all unique but not the smaller administrative layers. If you request a small area using name, make sure it's the one you are looking for before running your workflow. If it's not the case, use the :code:`get_names` method to get the administrative code associated to the requested names, they are all unique.

Let's demonstrate this behavior with the "Central" province of Singapore. First we try to load it using its name. It should return an error:

.. jupyter-execute::
    :raises: ValueError

    import pygadm

    gdf = pygadm.get_items(name="Central")

As I don't know the GADM code I copy/paste the suggested code from the error message and filter it by `country ISO alpha-3 code <https://www.iban.com/country-codes>`__. the ISO code is always displayed in the second column of the :code:`get_names` output. All GADM code start with the country ISO code so you can use the provided cell for any admin level.

.. jupyter-execute::

    import pygadm

    df = pygadm.get_names(name="Central")
    df = df[df.iloc[:,1].str.startswith("SGP")]
    df

I now know that the code is "SGP.1_1" for the Central province so I can run my initial code again with the unique :code:`admin` parameter:

.. jupyter-execute::

    import pygadm
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(admin="SGP.1_1")

    # display it in a map
    m = Map(basemap=basemaps.Esri.WorldImagery,  zoom=11, center=[1.29, 103.83])
    m.add(GeoJSON(data=gdf.__geo_interface__, style={"color": "red", "fillOpacity": .4}))

    m

Suggestion
----------

If you make an error when writing the name of your input, the error message will suggest 5 potential candidates in the existing names of the GADM dataset:


.. jupyter-execute::
    :raises: ValueError

    import pygadm

    gdf = pygadm.get_items(name="Franc")

