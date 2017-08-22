"""
Convert Catalogs to Pandas format for future usages.
Notes:
    1. Oklahoma catalog (OK) is used to generate event windows (positive
    detections)
    2. Benz catalog is more complete and used to generate noise windows (
    negative detections)
"""
import os
import sys
import numpy as np
import pandas as pd
from obspy import UTCDateTime

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(this_dir))

from convnetquake.aux_catalog import filter_catalog_time, filter_catalog_space


def load_OK_catalog(src, dst=None):
    src_cat = pd.read_csv(src)

    # Build new table
    count, _ = src_cat.shape
    utc_timestamp = [UTCDateTime(t).timestamp for t in src_cat['origintime']]
    label = np.zeros(count, dtype=int)
    latitude = src_cat['latitude']
    longitude = src_cat['longitude']
    depth = src_cat['depth']  # in km
    err_lat = src_cat['err_lat']  # in km
    err_lon = src_cat['err_lon']  # in km
    err_depth = src_cat['err_depth']  # in km

    cat = pd.DataFrame({
        'utc_timestamp': utc_timestamp,
        'latitude': latitude,
        'longitude': longitude,
        'depth': depth,
    })

    # Filter the events in cat to keep the events near Guthrie
    cat = filter_catalog_time(cat,
                              [UTCDateTime(2014, 2, 14, 0, 0),
                               UTCDateTime(2017, 1, 1, 0, 0)])

    cat = filter_catalog_space(cat,
                               [-97.6, -97.2],
                               [35.7, 36])

    if dst:
        cat.to_csv(dst)

    return cat


def load_Benz_catalog(src, dst=None):
    src_cat = pd.read_csv(src)

    utc_timestamp = [UTCDateTime(t).timestamp for t in src_cat['origintime']]
    mag = src_cat['Magnitude']

    df = pd.DataFrame({
        'utc_timestamp': utc_timestamp,
        'magnitude': mag
    })

    if dst:
        df.to_csv(dst)

    return df


if __name__ == '__main__':
    cat_file_OK = 'data/catalogs/OK_2014-2015-2016.csv'
    cat_OK = load_OK_catalog(cat_file_OK, 'tmp/catalog/OK.csv')
    print(cat_OK)

    cat_file_Benz = 'data/catalogs/Benz_catalog.csv'
    cat_Benz = load_Benz_catalog(cat_file_Benz, 'tmp/catalog/Benz.csv')
    print(cat_Benz)
