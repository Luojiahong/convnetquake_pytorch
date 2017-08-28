"""
Script to cut event windows from continuous mseed files according to OK
catalog and store each window in separated file in hdf5 format.
"""
import os
import sys
import argparse
import numpy as np
from obspy import UTCDateTime
from obspy.geodetics.base import gps2dist_azimuth
import deepdish as dd

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(this_dir))

from convnetquake.data_io import load_stream, load_catalog
from convnetquake.aux_catalog import filter_catalog_time


def compute_travel_time(src, dst, v):
    slon, slat, sdep = src
    dlon, dlat, ddep = dst

    hdist, _, _ = gps2dist_azimuth(slat, slon, dlat, dlon)
    hdist /= 1000  # Convert to km
    return np.sqrt(hdist ** 2 + (ddep - sdep) ** 2) / v


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
    tmp_root, tmp_file = os.path.split(args['dst'])
    dst_dir = "/".join((tmp_root, tmp_file))
    print(root, file, cat_file, dst_dir)

    # Open catalog
    cat = load_catalog(cat_file)

    # Extract station name
    sta, time = file.split('.')[0].split('_')
    # mn, yr = time.split('-')

    # Load stream
    st = load_stream('/'.join([root, file]))

    # search catalog
    filtered_cat = filter_catalog_time(cat,
                                       [st[0].stats.starttime,
                                        st[0].stats.endtime])

    for event_id, event_time in enumerate(
            filtered_cat['utc_timestamp']):
        dst_file = "_".join(["/".join((dst_dir, 'event')), str(sta),
                             str(UTCDateTime(event_time))]) + '.h5'

        # Compute travel time
        lon, lat, dep = filtered_cat.iloc[event_id][['longitude',
                                                     'latitude',
                                                     'depth']]
        travel_time = compute_travel_time((lon, lat, dep),
                                          (-97.454860, 35.796570, 0.333),
                                          5.0)

        st_event = st.slice(start_time, end_time)

        # Skip incomplete windows
        if st_event[0].data.shape[0] < 1000:
            continue

        # Skip zero windows
        if (st_event[0].data ** 2).sum() == 0:
            continue

        x_event = st_event[0].data[:1000]
        y_event = st_event[1].data[:1000]
        z_event = st_event[2].data[:1000]

        event_data = np.vstack((x_event, y_event, z_event))
        cluster_id = filtered_cat['cluster_id'].as_matrix()[event_id]

        dd.io.save(dst_file, (cluster_id, event_data))
