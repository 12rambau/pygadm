Usage
=====

Get items
--------- 

The PyGADM lib can be used to extract information from the GADM dataset as GeoPandas :code:`GeoDataFrame`.

countries
^^^^^^^^^

Using the :code:`get_items` methods, you can access the Administrative area using either its name or its GADM identification code. 

For exemple to extract the France map you can use the following code: 

.. jupyter-execute:: 

    import pygadm 
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(name="France")

    # display it in a map 
    m = Map(basemap=basemaps.Esri.WorldImagery)
    style = {"stroke": True, "color": "grey", "weight": 2, "opacity": 1, "fill": True, "fillColor": "grey", "fillOpacity": 0.4}
    m.add(GeoJSON(data=gdf.__geo_interface__, style=style))
    m

If you know the code of the area you try to use, you can use the GADM code instead of the name.

.. jupyter-execute:: 

    import pygadm 
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(admin="FRA")

    # display it in a map 
    m = Map(basemap=basemaps.Esri.WorldImagery)
    style = {"stroke": True, "color": "grey", "weight": 2, "opacity": 1, "fill": True, "fillColor": "grey", "fillOpacity": 0.4}
    m.add(GeoJSON(data=gdf.__geo_interface__, style=style))
    m


smaller admin levels
^^^^^^^^^^^^^^^^^^^^

One is not bind to only request a country, any level can be accesed using both names and/or GADM code. 

.. jupyter-execute:: 

    import pygadm 
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(name="Corse-du-Sud")

    # display it in a map 
    m = Map(basemap=basemaps.Esri.WorldImagery)
    style = {"stroke": True, "color": "grey", "weight": 2, "opacity": 1, "fill": True, "fillColor": "grey", "fillOpacity": 0.4}
    m.add(GeoJSON(data=gdf.__geo_interface__, style=style))
    m

.. warning:: 

    The names of countries are all unique but not the smaller administrative layer. If you request a small area using name, make sure it's the one you are looking for before running your workflow. If it's not the case, use the :code:`get_names` method to get the admin assosciated names.


content of an admin layer
^^^^^^^^^^^^^^^^^^^^^^^^^

using the :code:`content_level` option, one can require smaller administrative layer than the one setup in the name. For example when you request France, by setting up the :code:`content_level` option to 2, the geodataframe will include all the department geometries.

.. jupyter-execute:: 

    import pygadm 
    from ipyleaflet import GeoJSON, Map, basemaps

    gdf = pygadm.get_items(admin="FRA", content_level=2)

    # display it in a map 
    m = Map(basemap=basemaps.Esri.WorldImagery)
    style = {"stroke": True, "color": "grey", "weight": 2, "opacity": 1, "fill": True, "fillColor": "grey", "fillOpacity": 0.4}
    m.add(GeoJSON(data=gdf.__geo_interface__, style=style))
    m


find names
----------

To get the available name and GADM code in a administrative layer you can use the :code:`get_names` method with the same parameters. Use then these names in a :code:`get_items` request to get the geometry.

For example to the the name and codes of all the departments in France you can run: 

.. jupyter-execute::

    import pygadm

    pygadm.get_names(admin="FRA", content_level=2)

Google Earth engine
-------------------

If you want to use this lib with GEE, install the gee binding of the lib using: 

.. code-block:: console

    pip install pygadm[gee]

and then the gdf can automatically be transformed into a :code:`ee.FeatureCollection`: 

.. jupyter-execute::

    import pygadm
    import geemap

    fc = pygadm.get_items(admin="FRA", content_level=2).to_fc()

    # in this example we use geemap to dicplay the geometry on the map
    m = geemap.Map()
    m.addLayer(fc, {"color": "grey"}, "FRA")
    m



