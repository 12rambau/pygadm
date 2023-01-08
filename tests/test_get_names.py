import pytest

import pygadm


def test_empty():

    # request without something
    with pytest.raises(Exception):
        pygadm.get_names()


def test_duplicate_input():

    # request with too many things
    with pytest.raises(Exception):
        pygadm.get_names(name="Singapore", admin="SGP")


def test_nono_existing():

    # request non-existing area
    with pytest.raises(Exception):
        pygadm.get_names(name="t0t0")

    with pytest.raises(Exception):
        pygadm.get_names(admin="t0t0")


def test_area():

    # request an area
    sublevels = ["Singapore"]
    df = pygadm.get_names(name="Singapore")
    assert sorted(df.NAME_0.to_list()) == sublevels


def test_sub_content():

    # request a sublevel
    sublevels = ["Central", "East", "North", "North-East", "West"]
    df = pygadm.get_names(name="Singapore", content_level=1)
    assert len(df) == 5
    assert sorted(df.NAME_1.to_list()) == sublevels


def test_too_high():

    # request a too high level
    with pytest.warns(UserWarning):
        df = pygadm.get_names(admin="SGP.1_1", content_level=0)
        assert len(df) == 1
        assert df.NAME_1.to_list() == ["Central"]


def test_too_low():

    # request a level too low
    with pytest.warns(UserWarning):
        df = pygadm.get_names(admin="SGP.1_1", content_level=3)
        assert len(df) == 1
        assert df.NAME_1.to_list() == ["Central"]


def test_case_insensitive():

    df1 = pygadm.get_names(name="Singapore")
    df2 = pygadm.get_names(name="singaPORE")

    assert df1.equals(df2)
