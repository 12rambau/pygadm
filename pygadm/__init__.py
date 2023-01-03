import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

__version__ = "0.0.0"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"

__gadm_version__ = "410"  # 4.1
__gadm_url__ = "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_{}.gpkg"
__gadm_data__ = Path(__file__).parent / "data" / "gadm_database.parquet"


def get_items(
    name: str = "", admin: str = "", content_level: int = -1
) -> gpd.GeoDataFrame:
    """
    return the requested administrative boundary using the name or the administrative number

    Retrun an Geopandas Dataframe representing a administrative region. The region can be requested either by its "name" or it's "admin", the lib will identify its level on the fly. The user can also request for a specific level for its content e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. if Nothing is found the method will return an error.

    Args:
        name: The name of a administrative area. cannot be set along with :code:`id`.
        admin: the id of an administrative area in the GADM nomenclature. cannot be set along with :code:`name`.
        content_level: the level to use in the final dataset. Default to -1 (use level from the area)

    Returns:
        the dataframe of the requested area with all the GADM attributes
    """

    # sanitary check on parameters
    if name and admin:
        raise ValueError('"name" and "id" cannot be set at the same time.')
    elif not name and not admin:
        raise ValueError('at least "name" or "id" need to be set.')

    # set the id we look for and tell the function if its a name or an admin
    is_name = True if name else False
    id = name if name else admin

    # read the data and find if the element exist
    df = pd.read_parquet(__gadm_data__)
    column = "NAME_{}" if is_name else "GID_{}"
    is_in = df.filter([column.format(i) for i in range(6)]).isin([id])

    if not is_in.any().any():
        raise Exception(f'The requested "{id}" is not part of GADM')

    # Get the iso_3 of the associated country of the identifed area and the associated level
    line = is_in[~((~is_in).all(axis=1))].idxmax(1)
    index = line.index
    level = line.iloc[0][5 if is_name else 4]  # GID_ or NAME_
    iso_3 = df.loc[index, "GID_0"].array[0]

    # load the max_level available in the requested area
    sub_df = df[df[column.format(level)] == id]
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

    # read the data from server
    layer_name = f"ADM_ADM_{content_level}"
    level_gdf = gpd.read_file(__gadm_url__.format(iso_3), layer=layer_name)
    level_gdf.rename(columns={"COUNTRY": "NAME_0"}, inplace=True)
    gdf = level_gdf[level_gdf[column.format(level)] == id]

    return gdf


def get_names(name: str = "", admin: str = "", content_level: int = -1) -> pd.DataFrame:
    """
    return the list of names available in a administrative layer using the name or the administrative number

    Return a list of all the name contained in an administrative region. The region can be requested either by its "name" or it's "admin", the lib will identify its level on the fly. The user can also request for a specific level for its content e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. if Nothing is found the method will return an error.

    Args:
        name: The name of a administrative area. cannot be set along with :code:`id`.
        admin: the id of an administrative area in the GADM nomenclature. cannot be set along with :code:`name`.
        content_level: the level to use in the final dataset. Default to -1 (use level under the area)

    Returns:
        the list of all the available names
    """

    # sanitary check on parameters
    if name and admin:
        raise ValueError('"name" and "id" cannot be set at the same time.')
    elif not name and not admin:
        raise ValueError('at least "name" or "id" need to be set.')

    # set the id we look for and tell the function if its a name or an admin
    is_name = True if name else False
    id = name if name else admin

    # read the data and find if the element exist
    df = pd.read_parquet(__gadm_data__)
    column = "NAME_{}" if is_name else "GID_{}"
    is_in = df.filter([column.format(i) for i in range(6)]).isin([id])
    if not is_in.any().any():
        raise Exception(f'The requested "{id}" is not part of GADM')

    # Get the iso_3 of the associated country of the identifed area and the associated level
    line = is_in[~((~is_in).all(axis=1))].idxmax(1)
    level = line.iloc[0][5 if is_name else 4]  # GID_ or NAME_

    # load the max_level available in the requested area
    sub_df = df[df[column.format(level)] == id]
    max_level = next(i for i in reversed(range(6)) if (sub_df[f"GID_{i}"] != "").any())

    # get the request level from user
    if content_level == -1:
        content_level = int(level) + 1
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

    return sub_df[columns].drop_duplicates(ignore_index=True)
