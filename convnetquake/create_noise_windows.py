import os
import numpy as np
from obspy import UTCDateTime
import deepdish as dd
from convnetquake.data_io import load_stream, load_catalog
from convnetquake.aux_catalog import filter_catalog_time
from convnetquake.aux_stream import preprocess_stream

if __name__ == '__main__':
    # Open catalog
    cat = load_catalog('tmp/catalog/Benz.csv')

    # Load stream
    for root, dirs, files in os.walk('data/streams'):
        for file in files:
            sta, time = file.split('.')[0].split('_')
            mn, yr = time.split('-')

            # Only load data between 2/15/2014 and 8/31/2014
            if yr != '2014':
                continue

            if (float(mn) < 2) | (float(mn) > 8):
                continue

            print("Load data for {}/{} ...".format(mn, yr))

            # Load stream
            st = load_stream('/'.join([root, file]))

            # Preprocess stream
            st = preprocess_stream(st)

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
