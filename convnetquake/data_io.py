"""
Auxiliary functions for data I/O.
"""
from obspy import read
import pandas as pd


def load_stream(file):
    st = read(file)

    return st.merge(method=1, fill_value=0)


def load_catalog(file):
    cat = pd.read_csv(file)

    if 'utc_timestamp' not in cat.columns:
        raise ValueError("No UTC_timestamp. Check if catalog has been "
                         "converted.")

    return cat


if __name__ == '__main__':
    pass
