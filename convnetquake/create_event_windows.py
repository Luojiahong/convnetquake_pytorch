"""
Script to cut event windows from continuous mseed files according to OK
catalog and store each window in separated file in hdf5 format.
"""
import os
import sys
import numpy as np
from obspy import UTCDateTime
import deepdish as dd

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(this_dir))

from convnetquake.data_io import load_stream, load_catalog
from convnetquake.aux_catalog import filter_catalog_time
from convnetquake.aux_stream import preprocess_stream

if __name__ == '__main__':
    # Open catalog
    cat = load_catalog('tmp/catalog/OK_clustered.csv')

    # Load stream
    for root, dirs, files in os.walk('data/streams'):
        for file in files[:]:
            sta, time = file.split('.')[0].split('_')
            # mn, yr = time.split('-')

            # Load stream
            st = load_stream('/'.join([root, file]))

            # Preprocess stream
            st = preprocess_stream(st)

            # search catalog
            filtered_cat = filter_catalog_time(cat,
                                               [st[0].stats.starttime,
                                                st[0].stats.endtime])

            for event_id, event_time in enumerate(
                    filtered_cat['utc_timestamp']):
                dst_file = "_".join(['tmp/train/events/event', str(sta),
                                     str(UTCDateTime(event_time))]) + '.h5'

                # if os.path.exists(dst_file):
                #     continue

                start_time = UTCDateTime(event_time)
                end_time = start_time + 10
                st_event = st.slice(start_time, end_time)
                x_event = st_event[0].data[:1000]
                y_event = st_event[1].data[:1000]
                z_event = st_event[2].data[:1000]
                event_data = np.vstack((x_event, y_event, z_event))
                cluster_id = filtered_cat['cluster_id'].as_matrix()[event_id]

                dd.io.save(dst_file, (cluster_id, event_data))
