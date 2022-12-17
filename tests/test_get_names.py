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
        pygadm.get_names(name="toto")

    with pytest.raises(Exception):
        pygadm.get_names(admin="toto")


def test_area():

    # request an area
    sublevels = ["Central", "East", "North", "North-East", "West"]
    list_ = pygadm.get_names(name="Singapore")
    assert sorted(list_) == sublevels


def test_sub_content():

    # request a sublevel
    sublevels = ["Central", "East", "North", "North-East", "West"]
    list_ = pygadm.get_names(name="Singapore", content_level=1)
    assert len(list_) == 5
    assert sorted(list_) == sublevels


def test_too_high():

    # request a too high level
    with pytest.warns(UserWarning):
        list_ = pygadm.get_names(admin="SGP.1_1", content_level=0)
        assert len(list_) == 1
        assert list_ == ["Central"]


def test_too_low():

    # request a level too low
    with pytest.warns(UserWarning):
        list_ = pygadm.get_names(admin="SGP.1_1", content_level=3)
        assert len(list_) == 1
        assert list_ == ["Central"]
