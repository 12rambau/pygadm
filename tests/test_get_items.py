import math

import pytest

import pygadm


def test_empty():

    # request without something
    with pytest.raises(Exception):
        pygadm.get_items()


def test_duplicate_intput():

    # request with too many things
    with pytest.raises(Exception):
        pygadm.get_items(name="Singapore", admin="SGP")


def test_non_existing():

    # request non-existing area
    with pytest.raises(Exception):
        pygadm.get_items(name="t0t0")

    with pytest.raises(Exception):
        pygadm.get_items(admin="t0t0")


def test_area():

    # request an area
    bounds = [103.6091, 1.1664, 104.0858, 1.4714]
    gdf = pygadm.get_items(name="Singapore")
    assert gdf.loc[0]["GID_0"] == "SGP"
    assert all([math.isclose(b, t) for b, t in zip(gdf.total_bounds.tolist(), bounds)])


def test_sub_content():

    # request a sublevel
    sublevels = ["Central", "East", "North", "North-East", "West"]
    gdf = pygadm.get_items(name="Singapore", content_level=1)
    assert (gdf.GID_0 == "SGP").all()
    assert len(gdf) == 5
    assert sorted(gdf.NAME_1.to_list()) == sublevels


def test_too_high():

    # request a too high level
    with pytest.warns(UserWarning):
        gdf = pygadm.get_items(admin="SGP.1_1", content_level=0)
        assert len(gdf) == 1
        assert gdf.loc[0]["GID_1"] == "SGP.1_1"


def test_too_low():

    # request a level too low
    with pytest.warns(UserWarning):
        gdf = pygadm.get_items(admin="SGP.1_1", content_level=3)
        assert len(gdf) == 1
        assert gdf.loc[0]["GID_1"] == "SGP.1_1"


def test_case_insensitive():

    gdf1 = pygadm.get_items(name="Singapore")
    gdf2 = pygadm.get_items(name="singaPORE")

    assert gdf1.equals(gdf2)
