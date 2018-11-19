from load_data import load_data
import numpy as np
from sklearn.cluster import DBSCAN

def clustering(filename, epsilon=20):
    d = load_data(filename).dropna()

    cluster_finder = DBSCAN(eps=epsilon)

    d["rho"] = np.sqrt(d.x**2 + d.y**2)
    d["cluster_idx"] = cluster_finder.fit_predict(d[["rho", "z"]])

    means = list()

    for v in d["cluster_idx"].unique():
        # skip tracks belonging to no clusters
        if v==-1:
            continue
    
        x_mean = d.query("cluster_idx=={}".format(v)).x.mean()
        y_mean = d.query("cluster_idx=={}".format(v)).y.mean()
        z_mean = d.query("cluster_idx=={}".format(v)).z.mean()
        means.append((x_mean, y_mean, z_mean))
    
    return means