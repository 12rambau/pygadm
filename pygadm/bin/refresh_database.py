#!/usr/bin/python3

"""
Script to manually update the database of GADM

When GADM is releasing a new version the table should be updated to make sure that the names are still available in list and that new one are included. It is only meant to be executed by maintainer, Any PR included unwanted modifications to the database will be refused.
"""

import argparse
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

import geopandas as gpd
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
    # raise Exception(args)

    # url of the gadm files
    url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_{__gadm_version__}-gpkg.zip"

    # read the all the geodata available in the server at once
    with tempfile.TemporaryDirectory() as tmp_dir:

        # check if a download is required
        if vars(args)["gadm_src"] is not None:
            file = Path(vars(args)["gadm_src"])

        else:
            # get the file as a simple dataframe
            file = Path(tmp_dir) / urlparse(url).path.split("/")[-1]
            response = urlopen(url)
            pbar = tqdm(total=response.length, unit="iB", unit_scale=True)
            size = 16 * 1024
            with open(file, "wb") as f:
                while True:
                    chunk = response.read(size)
                    pbar.update(size)
                    if not chunk:
                        break
                    f.write(chunk)

        # read the file
        gadm_df = gpd.read_file(
            file, layer=f"gadm_{__gadm_version__}", ignore_geometry=True
        )

    # replace the country column by NAME_0 for coherence
    gadm_df.rename(columns={"COUNTRY": "NAME_0"}, inplace=True)

    # filter all columns but the GID and the NAME
    # we are not including the VARNAME to keep the file size under 3Mo
    columns = ["UID"]
    columns += [f"GID_{i}" for i in range(6)]
    columns += [f"NAME_{i}" for i in range(6)]
    gadm_df_filtered = gadm_df.filter(items=columns)

    # save it in the data folder
    filename = Path(__file__).parents[1] / "data" / "gadm_database.bz2"

    # specifying the protocol for compatibility with Python 3.7
    gadm_df_filtered.to_pickle(filename, protocol=4)
