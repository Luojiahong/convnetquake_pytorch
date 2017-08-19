"""
Convert Catalogs to Pandas format for future usages.
Notes:
    1. Oklahoma catalog (OK) is used to generate event windows (positive
    detections)
    2. Benz catalog is more complete and used to generate noise windows (
    negative detections)
"""

import numpy as np
import pandas as pd
from obspy import UTCDateTime


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

    df = pd.DataFrame({
        'utc_timestamp': utc_timestamp,
        'label': label,
        'latitude': latitude,
        'longitude': longitude,
        'depth': depth,
        'err_lat': err_lat,
        'err_lon': err_lon,
        'err_depth': err_depth})

    if dst:
        df.to_csv(dst)

    return df


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
