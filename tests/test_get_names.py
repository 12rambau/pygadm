"""Tests of the ``get_name`` function."""

import pytest

import pygadm


def test_empty():
    """Empty request."""
    with pytest.raises(Exception):
        pygadm.get_names()


def test_duplicate_input():
    """Request with too many parameters."""
    with pytest.raises(Exception):
        pygadm.get_names(name="Singapore", admin="SGP")


def test_non_existing():
    """Request non existing area."""
    with pytest.raises(Exception):
        pygadm.get_names(name="t0t0")

    with pytest.raises(Exception):
        pygadm.get_names(admin="t0t0")


def test_area():
    """Request a known."""
    sublevels = ["Singapore"]
    df = pygadm.get_names(name="Singapore")
    assert sorted(df.NAME_0.to_list()) == sublevels


def test_sub_content():
    """Request a sublevel."""
    sublevels = ["Central", "East", "North", "North-East", "West"]
    df = pygadm.get_names(name="Singapore", content_level=1)
    assert len(df) == 5
    assert sorted(df.NAME_1.to_list()) == sublevels


def test_too_high():
    """Request a sublevel higher than available in the area."""
    with pytest.warns(UserWarning):
        df = pygadm.get_names(admin="SGP.1_1", content_level=0)
        assert len(df) == 1
        assert df.NAME_1.to_list() == ["Central"]


def test_too_low():
    """Request a sublevel lower than available in the area."""
    with pytest.warns(UserWarning):
        df = pygadm.get_names(admin="SGP.1_1", content_level=3)
        assert len(df) == 1
        assert df.NAME_1.to_list() == ["Central"]


def test_case_insensitive():
    """Request an area without respecting the case."""
    df1 = pygadm.get_names(name="Singapore")
    df2 = pygadm.get_names(name="singaPORE")

    assert df1.equals(df2)
