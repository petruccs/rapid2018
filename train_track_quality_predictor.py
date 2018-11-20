
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn import tree
import json
from matplotlib import pyplot as plt
from pprint import pprint
import numpy as np
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

def getPVParams(track, mcps, mcvs):
    """ Given a track dict, the list of MCParticles and MCVertices 
    return the track PV position and ID (or None if not found or ambiguous)"""
    track_mcps = track['MCPs']
    # We ignore the tracks with no association to MCP or more than one
    if len(track_mcps) != 1:
        return None
    track_mcp = mcps[track_mcps[0]]
    track_pv_id = track_mcp['PV']
    track_pv = mcvs[track_pv_id]
    pos = track_pv['Pos']
    return pos[0], pos[1], pos[2], track_pv['key']


def getTrackFirstHitZ(track, hits):
    """ Returns the z of the first hit for the given track """
    hzs = [hits[h]['z'] for h in track['LHCbIDs']]
    return min(hzs), max(hzs)


def readData(filename, mycontainer):
    with open(filename) as mf:
        jdata = json.load(mf)
    # for key in jdata:
    #    print(key)
    VeloTracks = jdata['VeloTracks']
    VeloHits = jdata['VPClusters']
    mcps = jdata['MCParticles']
    mcvs = jdata['MCVertices']
    for l in VeloTracks.values():
        # if l['isBackwards']:
        #    continue
        pvps = getPVParams(l, mcps, mcvs)
        if pvps != None:
            mycontainer.append(l['ClosestToBeam'] + list(pvps) + [len(l['LHCbIDs'])]
                             + [*getTrackFirstHitZ(l, VeloHits)] + [jdata['EventNumber']])


def getzerr(row):
    # print(row)
    return row['pvz'] - row['z']


def isvalid(row):
    return (abs(row['zerr']) < 3.0)


def load_data(filelist, prefix="data/train"):

    container = []
    for fn in filelist:
        readData(os.path.join(prefix, fn), container)

    df = pd.DataFrame.from_records(container, columns=['x', 'y', 'z', 'tx', 'ty', 'qp', 'pvx', 'pvy', 'pvz',
                                                    'pvid', 'LHCbIDCount', 'first_hit_Z', 'last_hit_Z', 'EvtNum'])
    container[:] = []
    return df
    
    



logging.info("Loading data")
prefix="data/train"
trainfiles = os.listdir(prefix)[:]
df = load_data(trainfiles, prefix=prefix)


testprefix = "data/test"
testfiles = os.listdir(testprefix)[:]
df_test = load_data(testfiles, prefix=testprefix)


logging.info("Enhancing data with zerr and valid flag")


# Adding the error
df['zerr'] = df.apply(lambda row: getzerr(row), axis=1)
df_test['zerr'] = df_test.apply(lambda row: getzerr(row), axis=1)
df['valid'] = df.apply(lambda row: isvalid(row), axis=1)
df_test['valid'] = df.apply(lambda row: isvalid(row), axis=1)


logging.info("Training the classifier")
# And training
train_columns = [ 'z', 'tx', 'ty', 'first_hit_Z']
X = df.loc[:, train_columns]
y = df.loc[:, 'valid']

from sklearn.ensemble import RandomForestClassifier    
rfc = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
rfc.fit(X, y)


# Checking the classifier performance
logging.info("Checking the performance")
from sklearn.metrics import recall_score, precision_score, f1_score

X_test = df_test.loc[:, train_columns]
y_test = df_test.loc[:, 'valid']

y_pred = rfc.predict(X_test)

print(recall_score(y_test, y_pred))
print(precision_score(y_test, y_pred))
print(f1_score(y_test, y_pred))

logging.info("Saving the classifier")
from sklearn.externals import joblib
joblib.dump(rfc, 'track_classifier.joblib') 