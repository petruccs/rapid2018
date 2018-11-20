import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

CLUSTERING_KWARGS = {
    "epsilon": 5,
    "weight": "from_cov"
}

def clustering(X, epsilon=20, weight=None):

    cluster_finder = DBSCAN(eps=epsilon)
    X = X.dropna()

    X["rho"] = np.sqrt(X.x**2 + X.y**2)

    if weight is None:
        X["x_weight"] = np.ones(len(X))
        X["y_weight"] = np.ones(len(X))
        X["z_weight"] = np.ones(len(X))
    elif weight == "from_cov":
        X["x_weight"] = 1./ X.cov_x**2
        X["y_weight"] = 1. / X.cov_y**2
        X["z_weight"] = np.ones(len(X))
    else:
        raise RuntimeError("Dont know what to do with this weights")

    X["cluster_idx"] = cluster_finder.fit_predict(X[["rho", "z"]])

    means = list()

    for v in X["cluster_idx"].unique():
        # skip tracks belonging to no clusters
        if v==-1:
            continue

        dd = X[X.cluster_idx == v]
        x_mean = np.sum(dd.x * dd.x_weight) / dd.x_weight.sum()
        y_mean = np.sum(dd.y * dd.y_weight) / dd.y_weight.sum()
        z_mean = np.sum(dd.z * dd.z_weight) / dd.z_weight.sum()
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
        print(rv.shape)
        return rv
