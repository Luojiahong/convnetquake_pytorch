import numpy as np
from convnetquake.data_io import load_catalog
from matplotlib import pyplot as plt
from sklearn import cluster
import seaborn


def cluster_event(cat, dst=None, viz=False):
    # K-means
    lon = cat['longitude'].as_matrix()
    lat = cat['latitude'].as_matrix()
    samples = np.vstack((lon, lat)).T
    # print(samples)

    results = cluster.KMeans(n_clusters=6,
                             init=np.array([[-97.6, 36],
                                            [-97.4, 35.85],
                                            [-97.2, 35.85],
                                            [-97.3, 35.75],
                                            [-97.4, 35.95],
                                            [-97.6, 35.75]]),
                             n_init=10).fit(samples)

    # results = cluster.KMeans(n_clusters=6,
    #                          init='k-means++',
    #                          n_init=10).fit(samples)

    cluster_labels = results.labels_
    labels = list(set(cluster_labels))

    # Save results to catalog
    cat = cat.assign(cluster_id=cluster_labels)
    # print(cat)

    if dst:
        cat.to_csv(dst)

    # Visualize clustering results
    if viz:
        fig, ax = plt.subplots(1, 2, num=1, figsize=(8, 4), sharey=True)
        lat = cat.latitude
        lon = cat.longitude
        ax[0].scatter(lon, lat, s=5, color='k')
        ax[0].set_xlabel("Longitude (degree)")
        ax[0].set_ylabel("Latitude (degree)")
        ax[0].grid(True)

        # Display predicted scores by the model as contour plot
        x = np.linspace(lon.min(), lon.max(), 1000)
        y = np.linspace(lat.min(), lat.max(), 1000)
        X, Y = np.meshgrid(x, y)
        XX = np.array([X.ravel(), Y.ravel()]).T
        Z = results.predict(XX)
        Z = Z.reshape(X.shape)
        ax[1].contour(X, Y, Z, colors='k', levels=range(6))
        ax[1].set_xlabel("Longitude (degree)")

        # Add station on plot
        OK029_LAT = 35.796570
        OK029_LONG = -97.454860
        OK027_LAT = 35.72
        OK027_LONG = -97.29
        ax[0].plot(OK029_LONG, OK029_LAT, 'r*')
        ax[0].plot(OK027_LONG, OK027_LAT, 'r*')

        # plot the labels
        for label in labels:
            colors = seaborn.color_palette('hls', len(labels))[label]
            ax[1].scatter(lon[cluster_labels == label],
                          lat[cluster_labels == label],
                          s=5, c=colors, linewidth=0, label=label)
        ax[1].legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)

        plt.show()

    return cat


if __name__ == '__main__':
    # Open catalog
    catalog = load_catalog('tmp/catalog/OK.csv')
    catalog_clustered = cluster_event(catalog,
                                      dst='tmp/catalog/OK_clustered.csv',
                                      viz=False)
