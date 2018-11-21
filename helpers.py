import glob
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from scipy import signal
from sklearn.cluster import DBSCAN


def load_data(filename):
    with open(filename) as jsonfile:
        return json.load(jsonfile)


def extract_tracks(data):
    df = pd.DataFrame.from_dict(data['VeloTracks'], orient='index')
    df['x'] = df['ClosestToBeam'].map(lambda l: l[0])
    df['y'] = df['ClosestToBeam'].map(lambda l: l[1])
    df['z'] = df['ClosestToBeam'].map(lambda l: l[2])
    df['dx'] = df['ClosestToBeam'].map(lambda l: l[3])
    df['dy'] = df['ClosestToBeam'].map(lambda l: l[4])
    df['cov_x'] = df['errCTBState'].map(lambda l: l[0])
    df['cov_y'] = df['errCTBState'].map(lambda l: l[1])
    df['cov_dx'] = df['errCTBState'].map(lambda l: l[2])
    df['cov_dy'] = df['errCTBState'].map(lambda l: l[3])
    df['cov_xdx'] = df['errCTBState'].map(lambda l: l[4])
    df = df.drop('ClosestToBeam', axis=1).drop('errCTBState', axis=1)
    return df


def extract_mc(data):
    df = pd.DataFrame.from_dict(data['MCVertices'], orient='index')
    df['x'] = df['Pos'].map(lambda l: l[0])
    df['y'] = df['Pos'].map(lambda l: l[1])
    df['z'] = df['Pos'].map(lambda l: l[2])
    df = df.drop('Pos', axis=1)
    return df


def extract_mcpv(data):
    return pd.DataFrame.from_dict(data['MCParticles'], orient='index')


def extract_hits(data):
    return pd.DataFrame.from_dict(data['VPClusters'], orient='index')


def match_tracks_mc(tracks, hits, mcpv, mc, threshold=5):
    df = tracks[tracks['MCPs'].map(len) == 1].copy()
    df['MCP'] = df['MCPs'].map(lambda l: l[0])
    df['firstHit'] = df['LHCbIDs'].map(lambda l: l[0])
    df = df.merge(hits, left_on='firstHit', right_on='key', suffixes=('', 'FirstHit'))
    df = df.merge(mcpv[['PV', 'key']], left_on='MCP', right_on='key')
    df = df.merge(mc, left_on='PV', right_on='key', suffixes=('', 'PV'))
    df['zdiff'] = np.abs(df['z'] - df['zPV'])
    df['close'] = df['zdiff'] < threshold
    return df


def generate_features(df):
    df['rho'] = np.sqrt(df['x']**2 + df['y']**2)
    return df


def make_histogram(values, bins=None):
    if bins is None:
        bins = np.arange(-120, 120, 1)
    counts, edges = np.histogram(values, bins=bins)
    widths = edges[1:] - edges[:-1]
    centers = edges[:-1] + widths / 2
    return counts, centers, widths


def find_peaks(counts, centers, height=10):
    peaks, _ = signal.find_peaks(counts, height=height)
    return centers[peaks]


def find_clusters(zs, eps=1.5):
    return DBSCAN(eps=eps).fit_predict(zs)
