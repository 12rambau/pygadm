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

    # parse agruments
    parser.parse_args()

    # url of the gadm files
    url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_{__gadm_version__}-gpkg.zip"

    # read the all the geodata available in the server at once
    with tempfile.TemporaryDirectory() as tmp_dir:

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
        gadm_df = gpd.read_file(zip_file, ignore_geometry=True)

    # filter all columns but the GID and the NAME
    # we are not including the VARNAME to keep the file size under 3Mo
    columns = ["UID"]
    columns += [f"GID_{i}" for i in range(6)]
    columns += [f"NAME_{i}" for i in range(6)]
    gadm_df_filtered = gadm_df.filter(items=columns)

    # save it in the data folder
    filename = Path(__file__).parents[1] / "data" / "gadm_database.bz2"
    gadm_df_filtered.to_pickle(filename)
