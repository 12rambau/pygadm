"""
Easy access to administrative boundary defined by GADM from Python scripts.

This lib provides access to GADM datasets from a Python script without downloading the file from their server. We provide access to The current version (4.1.) which delimits 400,276 administrative areas.

The data are freely available for academic use and other non-commercial use. Redistribution, or commercial use is not allowed without prior permission. See the license of the GADM project for more details.
"""

import json
import warnings
from difflib import get_close_matches
from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import List, Union

import geopandas as gpd
import numpy as np
import pandas as pd
from deprecated.sphinx import deprecated, versionadded
from requests_cache import CachedSession

session = CachedSession("pygadm", use_temp=True)

__version__ = "0.5.2"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"

__gadm_version__ = "410"  # 4.1
__gadm_url__ = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{}_{}.json"
__gadm_data__ = Path(__file__).parent / "data" / "gadm_database.parquet"
__gadm_continent__ = json.loads(
    (Path(__file__).parent / "data" / "gadm_continent.json").read_text()
)


@lru_cache(maxsize=1)
def _df() -> pd.DataFrame:
    """Get the parquet database."""
    return pd.read_parquet(__gadm_data__)


@versionadded(version="0.5.2", reason="Add the Names class.")
class Names(pd.DataFrame):
    def __init__(
        self,
        name: str = "",
        admin: str = "",
        content_level: int = -1,
        complete: bool = False,
    ):
        """
        Set the list of names available in a administrative layer using the name or the administrative code.

        Return a pandas DataFrame of the names ad GADM code of an administrative region. The region can be requested either by its "name" or its "admin", the lib will identify the corresponding level on the fly. The user can also request for a specific level for its content e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. If Nothing is found the method will return an error.

        Args:
            name: The name of a administrative area. Cannot be set along with :code:`admin`.
            admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`.
            content_level: The level to use in the final dataset. Default to -1 (use level of the selected area).
            complete: If True, the method will return all the names of the higher administrative areas. Default to False.
        """
        # sanitary check on parameters
        if name and admin:
            raise ValueError('"name" and "id" cannot be set at the same time.')

        # if a name or admin number is set, we need to filter the dataset accordingly
        # if not we will simply consider the world dataset
        df = _df()
        if name or admin:
            # set the id we look for and tell the function if its a name or an admin
            is_name = True if name else False
            id = name if name else admin

            # read the data and find if the element exist
            column = "NAME_{}" if is_name else "GID_{}"
            is_in = (
                df.filter([column.format(i) for i in range(6)])
                .apply(lambda col: col.str.lower())
                .isin([id.lower()])
            )

            if not is_in.any().any():
                # find the 5 closest names/id
                columns = [
                    df[column.format(i)].dropna().str.lower().values for i in range(6)
                ]
                ids = np.unique(np.concatenate(columns))
                close_ids = get_close_matches(id.lower(), ids, n=5)
                if is_name is True:
                    close_ids = [i.capitalize() for i in close_ids]
                else:
                    close_ids = [i.upper() for i in close_ids]
                raise ValueError(
                    f'The requested "{id}" is not part of GADM. '
                    f'The closest matches are: {", ".join(close_ids)}.'
                )

            # Get the iso_3 of the associated country of the identifed area and the associated level
            line = is_in[~((~is_in).all(axis=1))].idxmax(1)
            level = line.iloc[0][5 if is_name else 4]  # GID_ or NAME_

            # load the max_level available in the requested area
            sub_df = df[df[column.format(level)].str.fullmatch(id, case=False)]
            max_level = next(
                i for i in reversed(range(6)) if (sub_df[f"GID_{i}"] != "").any()
            )

            # get the request level from user
            content_level, level = int(content_level), int(level)
            if content_level == -1:
                content_level = level
            elif content_level < level:
                warnings.warn(
                    f"The requested level ({content_level}) is higher than the area ({level}). "
                    f"Fallback to {level}."
                )
                content_level = level

            if content_level > max_level:
                warnings.warn(
                    f"The requested level ({content_level}) is higher than the max level in "
                    f"this country ({max_level}). Fallback to {max_level}."
                )
                content_level = max_level

        else:
            sub_df = df
            content_level = 0 if content_level == -1 else content_level

        # get the columns name to display
        columns = [f"NAME_{content_level}", f"GID_{content_level}"]

        # the list will contain duplicate as all the smaller admin level will be included
        sub_df = sub_df.drop_duplicates(subset=columns, ignore_index=True)

        # the list will contain NA as all the bigger admin level will be selected as well
        # the database is read as pure string so dropna cannot be used
        # .astype is also a vectorized operation so it goes very fast
        sub_df = sub_df[sub_df[columns[0]].astype(bool)]

        # filter the df if complete is set to False, the only displayed columns will be the one requested
        final_df = sub_df if complete is True else sub_df[columns]

        super().__init__(final_df)


@versionadded(version="0.5.2", reason="Add the Items class.")
class Items(gpd.GeoDataFrame):
    def __init__(
        self,
        name: Union[str, List[str]] = "",
        admin: Union[str, List[str]] = "",
        content_level: int = -1,
    ):
        """
        Return the requested administrative boundaries using the name or the administrative code.

        Return a Geopandas GeoDataFrame representing an administrative region. The region can be requested either by its "name" or its "admin", the lib will identify the area level on the fly. The user can also request for a specific level for the GeoDataFrame features e.g. get all admin level 1 of a country. If nothing is set we will infer the level of the item and if the level is higher than the found item, it will be ignored. If Nothing is found the method will return an error.

        Args:
            name: The name of an administrative area. Cannot be set along with :code:`admin`. it can be a list or a single name.
            admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`. It can be a list or a single admin code.
            content_level: The level to use in the final dataset. Default to -1 (use level from the area).
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
        gdf_list = [self._items(n, a, content_level) for a, n in product(admins, names)]

        # avoid concat if not needed for speed boost
        gdf = gdf_list[0] if len(gdf_list) == 1 else pd.concat(gdf_list)

        super().__init__(gdf)

    def _items(
        self, name: str = "", admin: str = "", content_level: int = -1
    ) -> gpd.GeoDataFrame:
        """
        Return the requested administrative boundaries from the single name or administrative code.

        Args:
            name: The name of an administrative area. Cannot be set along with :code:`admin`.
            admin: The id of an administrative area in the GADM nomenclature. Cannot be set along with :code:`name`.
            content_level: The level to use in the final dataset. Default to -1 (use level from the area).

        Returns:
            The GeoDataFrame of the requested area with all the GADM attributes.
        """
        # call to Names without level to raise an error if the requested level won't work
        df = Names(name, admin)
        if len(df) > 1:
            raise ValueError(
                f'The requested name ("{name}") is not unique ({len(df)} results). '
                'To retrieve it, please use the "admin" parameter instead. '
                "If you don't know the GADM code, use the following code, "
                f'it will return the GADM codes as well: "Names(name="{name}")"'
            )
        level = df.columns[0].replace("NAME_", "")
        iso_3 = df.iloc[0][f"GID_{level}"][:3]

        # now load the useful one to get content_level
        df = Names(name, admin, content_level)
        content_level = df.columns[0].replace("NAME_", "")

        # checks have already been performed in Names
        column = "NAME_{}" if name else "GID_{}"
        id = name if name else admin

        # read the data from server
        url = __gadm_url__.format(iso_3, content_level)
        try:
            data = json.loads(session.get(url).content)
        except Exception:
            # The data url is automatically build, it should be correct. From time
            # to time the server are down from GADM side so we write down a specific
            # error message if something goes wrong
            raise Exception(
                "We cannot retrieve the data from GADM server. "
                f"Try to manually open the following link: {url}. "
                "If it doesn't work, the error is coming from GADM servers. "
                "If it works please open an issue on our repository: https://github.com/12rambau/pygadm/issues."
            )

        level_gdf = gpd.GeoDataFrame.from_features(data)
        level_gdf.rename(columns={"COUNTRY": "NAME_0"}, inplace=True)
        gdf = level_gdf[level_gdf[column.format(level)].str.fullmatch(id, case=False)]

        # workaround for the wrong naming convention in the geojson files
        # https://gis.stackexchange.com/questions/467848/how-to-get-back-spaces-in-administrative-names-in-gadm-4-1
        # it should disappear in the next version of GADM
        # we are forced to retrieve all the names from the df (sourced from.gpkg) to replace the one from
        # the geojson that are all in camelCase
        complete_df = Names(name, admin, content_level=content_level, complete=True)
        for i in range(int(content_level) + 1):
            gdf.loc[:, (f"NAME_{i}")] = complete_df[f"NAME_{i}"].values

        return gdf


@deprecated(version="0.5.2", reason="Use the Names class instead.")
class AdmNames(Names):
    pass


@deprecated(version="0.5.2", reason="Use the Items class instead.")
class AdmItems(Items):
    pass


@deprecated(version="0.4.0", reason="Use the AdmItems class instead.")
def get_items(
    name: Union[str, List[str]] = "",
    admin: Union[str, List[str]] = "",
    content_level: int = -1,
) -> gpd.GeoDataFrame:
    """Return the requested administrative boundaries using the name or the administrative code."""
    return AdmItems(name, admin, content_level)


@deprecated(version="0.4.0", reason="Use the AdmNames class instead.")
def get_names(
    name: str = "", admin: str = "", content_level: int = -1, complete: bool = False
) -> pd.DataFrame:
    """Return the list of names available in a administrative layer using the name or the administrative code."""
    return AdmNames(name, admin, content_level, complete)
