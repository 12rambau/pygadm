"""Tests of the continents submanagement."""
import json
from pathlib import Path

import pandas as pd

import pygadm

continent_file = Path(__file__).parents[1] / "pygadm" / "data" / "gadm_continent.json"
database_file = Path(__file__).parents[1] / "pygadm" / "data" / "gadm_database.parquet"


def test_file():
    """Assert the continent file exist."""
    assert continent_file.is_file()


def test_continent(dataframe_regression):
    """Check that the continent are working on the simplest."""
    gdf = pygadm.get_items(name="antartica")
    df = pd.concat([gdf.GID_0, gdf.bounds], axis=1)
    dataframe_regression.check(df)


def test_duplication():
    """Make sure there are no duplicates in the continent database."""
    continent_dict = json.loads(continent_file.read_text())
    duplicates = {}
    for continent in continent_dict:
        duplicates[continent] = set()
        current_set = set(continent_dict[continent])
        for other in continent_dict:
            if other == continent:
                continue
            other_list = continent_dict[other]
            intersection = current_set.intersection(other_list)
            duplicates[continent] = duplicates[continent].union(intersection)

    error = [f"{c}: [{','.join(d)}]" for c, d in duplicates.items()]
    assert all([len(d) == 0 for c, d in duplicates.items()]), error


def test_orphan():
    """Check that all countries are in a continent."""
    data = pd.read_parquet(database_file)
    continent_dict = json.loads(continent_file.read_text())
    countries = data.GID_0.unique()
    orphan = []
    for country in countries:
        exist = False
        for continent in continent_dict:
            if country in continent_dict[continent]:
                exist = True
                break
        if exist is False:
            orphan.append(country)
    assert len(orphan) == 0, ",".join(orphan)
