import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from pprint import pprint

CLUSTERING_KWARGS = {
    "eps": 0.4, #1.625,
    # "weight": "from_cov"
    "n_jobs": 2
}

def clustering(X, weight=None, **kwargs):
    # X = X.dropna()
    # d = pd.DataFrame()
    # d["rho"] = np.sqrt(X.x**2 + X.y**2)
    # d["x"] = X.x
    # d["y"] = X.y
    # d["z"] = X.z
    # d["cov_x"] = X.cov_x
    # d["cov_y"] = X.cov_y

    d = X.dropna()

    from sklearn.neighbors import LocalOutlierFactor
    lof = LocalOutlierFactor(contamination="auto")
    d["outlier"] = lof.fit_predict(d[["x", "y", "z"]])

    d = d[d.outlier>0]

    cluster_finder = DBSCAN(**kwargs)




    d["rho"] = np.sqrt(X.x**2 + X.y**2)
    if weight is None:
        d["x_weight"] = np.ones(len(d))
        d["y_weight"] = np.ones(len(d))
        d["z_weight"] = np.ones(len(d))
    elif weight == "from_cov":
        d["x_weight"] = 1./ d.cov_x**2
        d["y_weight"] = 1. / d.cov_y**2
        d["z_weight"] = np.ones(len(d))
    else:
        raise RuntimeError("Dont know what to do with this weights")

    d["cluster_idx"] = cluster_finder.fit_predict(
        d[["x", "y", "z"]]
        # X.z.values.reshape(-1, 1)
    )

    means = list()

    for v in d["cluster_idx"].unique():
        # skip tracks belonging to no clusters
        if v==-1:
            continue

        dd = d[d.cluster_idx == v]
        x_mean = np.sum(dd.x * dd.x_weight) / np.sum(dd.x_weight)
        y_mean = np.sum(dd.y * dd.y_weight) / np.sum(dd.y_weight)
        z_mean = np.sum(dd.z * dd.z_weight) / np.sum(dd.z_weight)
        means.append((x_mean, y_mean, z_mean))
    return means


class ObjectDetector:
    def __init__(self):
        pass

    def fit(self, X, y):
        return self

    def predict(self, X):
        PVs = list()
        for event in X:
            df = pd.DataFrame()
            x_ = list()
            y_ = list()
            z_ = list()
            cov_x_ = list()
            cov_y_ = list()
            for velo_state in event.tracks:
                x_.append(velo_state.x)
                y_.append(velo_state.y)
                z_.append(velo_state.z)
                cov_x_.append(velo_state.cov_x)
                cov_y_.append(velo_state.cov_y)

            df["x"] = x_
            df["y"] = y_
            df["z"] = z_
            df["cov_x"] = cov_x_
            df["cov_y"] = cov_y_

            PVs += [clustering(df, **CLUSTERING_KWARGS)]

        rv = np.empty(len(PVs), dtype=object)
        rv[:] = PVs
        
        return rv
