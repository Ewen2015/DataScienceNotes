import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pylab as plt

def Elbow(data, clusters_range=range(1, 10)):
    clusters_range = clusters_range
    meandist = []
    pass

    for k in clusters_range,:
        model = KMeans(n_clusters=k)
        model.fit(data)
        meandist.append(sum(np.min(cdist(data, model.cluster_centers_, 'euclidean'), axis=1)) / data.shape[0])

    plt.figure(figsize=(8, 7))
    plt.plot(clusters_range, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method')
    plt.show()
    return None

def KMeansPCA(data, n_clusters=3):
    model = KMeans(n_clusters=n_clusters)
    model.fit(data)

    pca_2 = PCA(2)
    plot_columns = pca_2.fit_transform(data)

    plt.figure(figsize=(8,7))
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=model.labels_)
    plt.xlabel('Canonical variable 1')
    plt.ylabel('Canonical variable 2')
    plt.title('Scatterplot for Canonical Variables for '+n_clusters+' Clusters')
    plt.show()
    return None