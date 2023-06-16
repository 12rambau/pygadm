"""
Easy access to administrative boundary defined by GADM from Python scripts.

This lib provides access to GADM datasets from a Python script without downloading the file from their server. We provide access to The current version (4.1.) which delimits 400,276 administrative areas.

The data are freely available for academic use and other non-commercial use. Redistribution, or commercial use is not allowed without prior permission. See the license of the GADM project for more details.
"""

import json
import warnings
from itertools import product
from pathlib import Path
from typing import List, Union

import geopandas as gpd
import pandas as pd

__version__ = "0.2.0"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"

__gadm_version__ = "410"  # 4.1
__gadm_url__ = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{}_{}.json"
__gadm_data__ = Path(__file__).parent / "data" / "gadm_database.parquet"
__gadm_continent__ = json.loads(
    (Path(__file__).parent / "data" / "gadm_continent.json").read_text()
)

# __all__ = ["get_items", "get_names"]


def get_items(
    name: Union[str, List[str]] = "",
    admin: Union[str, List[str]] = "",
    content_level: int = -1,
) -> gpd.GeoDataFrame:
    """
    Return the requested administrative boundaries using the name or the administrative code.

    Return a Geopandas GeoDataFrame representing an administrative region. The region can be requested either by its "name" or its "admin", the lib will identify the area level on the fly. The user can also request for a specific level for the GeoDataFrame features e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. If Nothing is found the method will return an error.

    Args:
        name: The name of an administrative area. Cannot be set along with :code:`admin`. it can be a list or a single name.
        admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`. It can be a list or a single admin code.
        content_level: The level to use in the final dataset. Default to -1 (use level from the area).

    Returns:
        The GeoDataFrame of the requested area with all the GADM attributes.
    """
    # set up the loop
    names = [name] if isinstance(name, str) else name
    admins = [admin] if isinstance(admin, str) else admin

    # check that they are not all empty
    if names == [""] == admins:
        raise ValueError('at least "name" or "admin" need to be set.')

    # special parsing for continents. They are saved as admins to avoid any duplication
    if len(names) == 1 and names[0].lower() in __gadm_continent__:
        admins = [c for c in __gadm_continent__[names[0].lower()]]
        names = [""]

    # use itertools, normally one of them is empty so it will raise an error
    # if not the case as admin and name will be set together
    gdf_list = [_items(n, a, content_level) for a, n in product(admins, names)]

    # avoid concat if not needed for speed boost
    gdf = gdf_list[0] if len(gdf_list) == 1 else pd.concat(gdf_list)

    return gdf


def _items(
    name: str = "", admin: str = "", content_level: int = -1
) -> gpd.GeoDataFrame:
    """
    Return the requested administrative boundaries using the name or the administrative code.

    Same method as get_items but only accept single requests in str format.

    Args:
        name: The name of an administrative area. Cannot be set along with :code:`admin`.
        admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`.
        content_level: The level to use in the final dataset. Default to -1 (use level from the area).

    Returns:
        The GeoDataFrame of the requested area with all the GADM attributes.
    """
    # call to get_names without level to raise an error if the requested level won't work
    df = get_names(name, admin)
    if len(df) > 1:
        raise ValueError(
            f'The requested name ("{name}") is not unique ({len(df)} results). To retreive it, please use the `admin` parameter instead. If you don\'t know the GADM code, use the following code, it will return the GADM codes as well:\n`get_names(name="{name}")`'
        )
    level = df.columns[0].replace("NAME_", "")
    iso_3 = df.iloc[0][f"GID_{level}"][:3]

    # now load the usefull one to get content_level
    df = get_names(name, admin, content_level)
    content_level = df.columns[0].replace("NAME_", "")

    # checks have already been performed in get_names
    column = "NAME_{}" if name else "GID_{}"
    id = name if name else admin

    # read the data from server
    url = __gadm_url__.format(iso_3, content_level)
    try:
        level_gdf = gpd.read_file(url)
    except Exception as e:
        # The data url is automatically build, it should be correct. From time
        # to time the server are down from GADM side so we wrie down a specific
        # error message if something goes wrong
        raise Exception(f"We cannot retreive the data from GADM server. Try to manually open the following link: {url}. If it doesn't work, the error is coming from GADM servers. If it works please open an issue on our repository: https://github.com/12rambau/pygadm/issues.")

    level_gdf.rename(columns={"COUNTRY": "NAME_0"}, inplace=True)
    gdf = level_gdf[level_gdf[column.format(level)].str.fullmatch(id, case=False)]

    return gdf


def get_names(name: str = "", admin: str = "", content_level: int = -1) -> pd.DataFrame:
    """
    Return the list of names available in a administrative layer using the name or the administrative code.

    Return a pandas DataFrame of the names ad GADM code of an administrative region. The region can be requested either by its "name" or its "admin", the lib will identify the coresponding level on the fly. The user can also request for a specific level for its content e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. If Nothing is found the method will return an error.

    Args:
        name: The name of a administrative area. Cannot be set along with :code:`admin`.
        admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`.
        content_level: The level to use in the final dataset. Default to -1 (use level of the selected area).

    Returns:
        The list of all the available names.
    """
    # sanitary check on parameters
    if name and admin:
        raise ValueError('"name" and "id" cannot be set at the same time.')
    elif not name and not admin:
        raise ValueError('at least "name" or "admin" need to be set.')

    # set the id we look for and tell the function if its a name or an admin
    is_name = True if name else False
    id = name if name else admin

    # read the data and find if the element exist
    df = pd.read_parquet(__gadm_data__)
    column = "NAME_{}" if is_name else "GID_{}"
    is_in = (
        df.filter([column.format(i) for i in range(6)])
        .apply(lambda col: col.str.lower())
        .isin([id.lower()])
    )

    if not is_in.any().any():
        raise Exception(f'The requested "{id}" is not part of GADM')

    # Get the iso_3 of the associated country of the identifed area and the associated level
    line = is_in[~((~is_in).all(axis=1))].idxmax(1)
    level = line.iloc[0][5 if is_name else 4]  # GID_ or NAME_

    # load the max_level available in the requested area
    sub_df = df[df[column.format(level)].str.fullmatch(id, case=False)]
    max_level = next(i for i in reversed(range(6)) if (sub_df[f"GID_{i}"] != "").any())

    # get the request level from user
    if content_level == -1:
        content_level = level
    elif content_level < int(level):
        warnings.warn(
            f"The requested level ({content_level}) is higher than the area ({level}). Fallback to {level}."
        )
        content_level = level

    if int(content_level) > max_level:
        warnings.warn(
            f"The requested level ({content_level}) is higher than the max level in this country ({max_level}). Fallback to {max_level}."
        )
        content_level = max_level

    # get the columns name to display
    columns = [f"NAME_{content_level}", f"GID_{content_level}"]

    # the list will contain duplicate as all the smaller admin level will be included
    sub_df = sub_df[columns].drop_duplicates(ignore_index=True)

    # the list will contain NA as all the bigger admin level will be selected as well
    # the database is read as pure string so dropna cannot be used
    # .astype is also a vectorized operation so it goes very fast
    final_df = sub_df[sub_df[columns[0]].astype(bool)]

    return final_df
