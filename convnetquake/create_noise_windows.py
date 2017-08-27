import os
import sys
import argparse
import numpy as np
from obspy import UTCDateTime
import deepdish as dd
import warnings

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(this_dir))

from convnetquake.data_io import load_stream, load_catalog
from convnetquake.aux_catalog import filter_catalog_time

if __name__ == '__main__':
    # ============================ Parse Args ==============================
    # Read args
    parser = argparse.ArgumentParser(description='Prepare noise windows')
    parser.add_argument('-s', '--src', help='Source file location',
                        required=True)
    parser.add_argument('-d', '--dst', help='Destination files location',
                        required=True)
    parser.add_argument('-c', '--catalog', help='Catalog files location',
                        required=True)
    args, unknown = parser.parse_known_args()
    args = vars(args)

    print(args, unknown)

    # Assign args
    root, file = os.path.split(args['src'])
    cat_file = args['catalog']
    print(root, file, cat_file)

    sta, time = file.split('.')[0].split('_')
    mn, yr = time.split('-')

    # =========== Only load data between 2/15/2014 and 8/31/2014 ===========
    msg = "Current file {} is outside the interest region".format(file)
    if yr != '2014':
        # continue
        warnings.warn(msg)
        sys.exit(0)

    if (float(mn) < 2) | (float(mn) > 8):
        # continue
        warnings.warn(msg)
        sys.exit(0)

    # ==================== Load data ====================
    # Open catalog
    cat = load_catalog(cat_file)

    print("Load data for {}/{} ...".format(mn, yr))

    # Load stream
    st = load_stream('/'.join([root, file]))

    for st_window in st.slide(window_length=10, step=10):
        # Window start and end time
        window_start_time = st_window[0].stats.starttime
        window_end_time = st_window[0].stats.endtime

        # Remove data before 2/15/2014
        if window_start_time < UTCDateTime(2014, 2, 15, 0, 0):
            continue

        # search catalog
        filtered_cat = filter_catalog_time(cat,
                                           [window_start_time - 10,
                                            window_end_time + 10])
        if filtered_cat.empty:  # No event
            x_noise = st_window[0].data[:1000]
            y_noise = st_window[1].data[:1000]
            z_noise = st_window[2].data[:1000]
            noise_data = np.vstack((x_noise, y_noise, z_noise))

            dst_file = "_".join(['tmp/train/noises/noise',
                                 str(sta),
                                 str(UTCDateTime(window_start_time))
                                 ]) + '.h5'
            dd.io.save(dst_file, (-1, noise_data))
