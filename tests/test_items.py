"""Tests of the ``get_items`` function."""

import pandas as pd
import pytest

import pygadm


def test_empty():
    """Empty request."""
    with pytest.raises(Exception):
        pygadm.Items()


def test_duplicate_intput():
    """Request with too many parameters."""
    # request with too many things
    with pytest.raises(Exception):
        pygadm.Items(name="Singapore", admin="SGP")


def test_non_existing():
    """Request non existing area."""
    with pytest.raises(Exception):
        pygadm.Items(name="t0t0")

    with pytest.raises(Exception):
        pygadm.Items(admin="t0t0")


def test_area(dataframe_regression):
    """Request a known geometry."""
    gdf = pygadm.Items(name="Singapore")
    df = pd.concat([gdf.GID_0, gdf.bounds], axis=1)
    dataframe_regression.check(df)


def test_sub_content(dataframe_regression):
    """Request a sublevel."""
    gdf = pygadm.Items(name="Singapore", content_level=1)
    dataframe_regression.check(gdf[["NAME_1", "GID_0"]])


def test_too_high(data_regression):
    """Request a sublevel higher than available in the area."""
    with pytest.warns(UserWarning):
        gdf = pygadm.Items(admin="SGP.1_1", content_level=0)
        data_regression.check(gdf.GID_1.tolist())


def test_too_low(data_regression):
    """Request a sublevel lower than available in the area."""
    # request a level too low
    with pytest.warns(UserWarning):
        gdf = pygadm.Items(admin="SGP.1_1", content_level=3)
        data_regression.check(gdf.GID_1.tolist())


def test_case_insensitive():
    """Request an area without respecting the case."""
    gdf1 = pygadm.Items(name="Singapore")
    gdf2 = pygadm.Items(name="singaPORE")

    assert gdf1.equals(gdf2)


def test_duplicate_areas():
    """Test that duplicate geometries return an error."""
    with pytest.raises(ValueError):
        pygadm.Items(name="central")


def test_multiple_input(dataframe_regression):
    """Test when several geometries are requested at once."""
    gdf1 = pygadm.Items(name=["france", "germany"])
    df = pd.concat([gdf1.GID_0, gdf1.bounds], axis=1)
    dataframe_regression.check(df)

    gdf2 = pygadm.Items(admin=["FRA", "DEU"])
    assert gdf2.equals(gdf1)


def test_duplication(data_regression):
    """Test that known duplication cases return the biggest AOI."""
    # italy is also a level 4 province of Bangladesh: BGD.5.4.6.6_1
    gdf = pygadm.Items(name="Italy")
    data_regression.check(gdf.GID_0.tolist())


def test_camelCase_names(data_regression):
    """Test that camelCase names are replaced."""
    gdf = pygadm.Items(admin="COD", content_level=1)
    data_regression.check(gdf.NAME_0.tolist())


def test_get_items():
    """Test the get_items function."""
    gdf1 = pygadm.Items(name="Singapore")

    with pytest.warns(DeprecationWarning):
        gdf2 = pygadm.get_items(name="Singapore")
        assert gdf1.equals(gdf2)


def test_adm_items():
    """Test the AdmItems class."""
    gdf1 = pygadm.Items(name="Singapore")

    with pytest.warns(DeprecationWarning):
        gdf2 = pygadm.AdmItems(name="Singapore")
        assert gdf1.equals(gdf2)
