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
        pygadm.get_items(name="toto")

    with pytest.raises(Exception):
        pygadm.get_items(admin="toto")


def test_area():

    # request an area
    bounds = [
        103.60905500000018,
        1.1663900010000248,
        104.08580000000006,
        1.471388000000104,
    ]
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
