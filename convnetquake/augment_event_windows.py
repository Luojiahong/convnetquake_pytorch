import os
import argparse
import numpy as np
import deepdish as dd

if __name__ == '__main__':
    # File names
    src_dir = "tmp/train/events"
    dst_dir = "tmp/train/augmented_events"

    # ============================ Parse Args ==============================
    # Read args
    parser = argparse.ArgumentParser(description='Prepare noise windows')
    parser.add_argument('-s', '--src', help='Source file location',
                        required=True)
    parser.add_argument('-d', '--dst', help='Destination files location',
                        required=True)
    args, unknown = parser.parse_known_args()
    args = vars(args)

    print(args, unknown)

    # Assign args
    src_root, src_file = os.path.split(args['src'])
    dst_root, dst_file = os.path.split(args['dst'])
    # Remove '/' at the end
    src_dir = "/".join((src_root, src_file))
    dst_dir = "/".join((dst_root, dst_file))
    print(src_dir, dst_dir)

    # Noise levels
    SNR_list = range(1, 21)

    for root, dirs, files in os.walk(src_dir):
        for i, file in enumerate(files):
            # Load file
            label, data_mtx = dd.io.load("/".join((root, file)))
            # print(label, data_mtx)

            signal_std = np.std(data_mtx, axis=1).min()

            # Add noise
            for snr in SNR_list:
                noise_std = signal_std * 10 ** (snr / 20)
                new_data_mtx = data_mtx + np.random.normal(0,
                                                           noise_std,
                                                           data_mtx.shape)
                dst_file = "/".join([dst_dir,
                                     "_".join([file.split('.')[0],
                                               'snr',
                                               str(snr),
                                               'dB'])]) + '.h5'
                dd.io.save(dst_file, (label, new_data_mtx))

