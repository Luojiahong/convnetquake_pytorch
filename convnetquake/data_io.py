"""
Auxiliary functions for data I/O.
"""
import os
from obspy import read
import pandas as pd
from torch.utils.data.dataset import Dataset
from deepdish.io import load


def load_stream(file):
    st = read(file)
    st.detrend('constant')
    st.normalize()

    return st.merge(method=1, fill_value=0)


def load_catalog(file):
    cat = pd.read_csv(file)

    if 'utc_timestamp' not in cat.columns:
        raise ValueError("No UTC_timestamp. Check if catalog has been "
                         "converted.")

    return cat


class OKDataset(Dataset):
    def __init__(self, data_dir):
        self.data_files = []
        for root, dirs, files in os.walk(data_dir):
            self.data_files += files
        self.data_files.sort()

    def __getindex__(self, idx):
        # output in (label, data) tuple
        return load(self.data_files[idx])

    def __len__(self):
        return len(self.data_files)


if __name__ == '__main__':
    pass
