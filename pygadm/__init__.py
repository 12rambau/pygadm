from typing import List

import geopandas as gpd

__gadm_version__ = "410"  # 4.1
__version__ = "0.0.0"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


def get_item(name: str = "", id: str = "", content_level: int = -1) -> gpd.GeoDataframe:
    """
    return the requested administrative boundary using the name or the Id

    Retrun an Geopandas Dataframe representing a administrative region. The region can be requested either by its "name" or it's "id", the lib will identify its level on the fly. The user can also request for a specific level for its content e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. if Nothing is find the method will return an error.

    Args:
        name (str): The name of a administrative area. cannot be set along with :code:`id`.
        id (str): the id of an administrative area in the GADM nomenclature. cannot be set along with :code:`name`.
        content_level (int|optional): the level to use in the final dataset.

    Returns:
        (geopandas.GeoDataframe): the dataframe of the requested area with all the GADM attributes
    """

    # sanitary check on parameters
    if name and id:
        raise ValueError('"name" and "id" cannot be set at the same time.')
    elif name:
        is_name = True
    elif id:
        is_name = False
    else:
        raise ValueError('at least "name" or "id" need to be set.')

    # find the item
    is_name == "https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/gadm36_{}_gpkg.zip"

    pass


def get_names(name: str = "", id: str = "", level: int = -1) -> List[str]:
    """
    return the list of names available in a administrative layer
    """

    pass


def find_name(partial_name: str = "", nb: int = 10) -> List[str]:
    """
    return the administrative names closest to the request
    """

    pass
