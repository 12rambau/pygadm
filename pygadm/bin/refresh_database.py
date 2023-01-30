#!/usr/bin/python3

"""
Script to manually update the database of GADM.

When GADM is releasing a new version the table should be updated to make sure that the names are still available in list and that new one are included. It is only meant to be executed by maintainer, Any PR included unwanted modifications to the database will be refused.
"""

import argparse
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

import geopandas as gpd
import pandas as pd
from tqdm import tqdm

from pygadm import __gadm_version__

parser = argparse.ArgumentParser(description=__doc__, usage="refresh_database")

if __name__ == "__main__":

    # read arguments
    parser.add_argument(
        "-f",
        dest="gadm_src",
        metavar="source.gpkg",
        help="(str) : path to the GADM file",
        required=False,
        type=Path,
    )

    # parse agruments
    args = parser.parse_args()

    # url of the gadm files
    url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_{__gadm_version__}-level.zip"

    # read the all the geodata available in the server at once
    with tempfile.TemporaryDirectory() as tmp_dir:

        # check if a download is required
        if vars(args)["gadm_src"] is not None:
            zip_file = Path(vars(args)["gadm_src"])

        else:
            # get the file as a simple dataframe
            zip_file = Path(tmp_dir) / urlparse(url).path.split("/")[-1]
            response = urlopen(url)
            pbar = tqdm(total=response.length, unit="iB", unit_scale=True)
            size = 16 * 1024
            with open(zip_file, "wb") as f:
                while True:
                    chunk = response.read(size)
                    pbar.update(size)
                    if not chunk:
                        break
                    f.write(chunk)

        # unzip file
        file = Path(tmp_dir) / f"gadm_{__gadm_version__}-levels.gpkg"
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(Path(tmp_dir))

        # read the file layer by layer
        gid_0 = gpd.read_file(file, layer="ADM_0", ignore_geometry=True)
        gid_1 = gpd.read_file(file, layer="ADM_1", ignore_geometry=True)
        gid_2 = gpd.read_file(file, layer="ADM_2", ignore_geometry=True)
        gid_3 = gpd.read_file(file, layer="ADM_3", ignore_geometry=True)
        gid_4 = gpd.read_file(file, layer="ADM_4", ignore_geometry=True)
        gid_5 = gpd.read_file(file, layer="ADM_5", ignore_geometry=True)

        # concatenate all the df in area size order
        df = pd.concat([gid_0, gid_1, gid_2, gid_3, gid_4, gid_5])

    # change database structure to meet pygadm requirements
    df = df.fillna("").rename(columns={"COUNTRY": "NAME_0"})

    # filter all columns but the GID and the NAME
    # we are not including the VARNAME to keep the file size under 3Mo
    columns = ["UID"]
    columns += [f"GID_{i}" for i in range(6)]
    columns += [f"NAME_{i}" for i in range(6)]
    df_filtered = df.filter(items=columns)

    # save it in the data folder
    filename = Path(__file__).parents[1] / "data" / "gadm_database.parquet"

    # specifying the protocol for compatibility with Python 3.7
    df_filtered.to_parquet(filename, compression="Brotli")
