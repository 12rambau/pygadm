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


def test_area(dataframe_regression):
    """Request a known geometry."""
    df = pygadm.get_names(name="Singapore")
    dataframe_regression.check(df)

    df_admin = pygadm.get_names(admin="SGP")
    assert df_admin.equals(df)


def test_sub_content(dataframe_regression):
    """Request a sublevel."""
    df = pygadm.get_names(name="Singapore", content_level=1)
    dataframe_regression.check(df)


def test_too_high(dataframe_regression):
    """Request a sublevel higher than available in the area."""
    with pytest.warns(UserWarning):
        df = pygadm.get_names(admin="SGP.1_1", content_level=0)
        dataframe_regression.check(df)


def test_too_low(dataframe_regression):
    """Request a sublevel lower than available in the area."""
    with pytest.warns(UserWarning):
        df = pygadm.get_names(admin="SGP.1_1", content_level=3)
        dataframe_regression.check(df)


def test_case_insensitive():
    """Request an area without respecting the case."""
    df1 = pygadm.get_names(name="Singapore")
    df2 = pygadm.get_names(name="singaPORE")

    assert df1.equals(df2)


def test_duplication():
    """Test that known duplication cases return the biggest AOI."""
    # italy is also a level 4 province of Bangladesh: BGD.5.4.6.6_1
    df = pygadm.get_names(name="Italy")
    assert df.GID_0.to_list() == ["ITA"]


def test_suggestions():
    """Test that when a wrong name is given 5 options are proposed in the error message."""
    expected_error = 'The requested "Franc" is not part of GADM. The closest matches are: Francs, Franco, France, Franca, Francon.'
    with pytest.raises(ValueError, match=expected_error):
        pygadm.get_names(name="Franc")
