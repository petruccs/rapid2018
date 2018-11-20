import helpers as helpers
import pandas as pd
import glob
import os

def dump_tracks(readPath = 'data/train/', writePath = './json/'):
    if not os.path.exists(writePath):
        os.mkdir(writePath)
    files = glob.glob(readPath + '*.json')

    for name in files:
        data = helpers.load_data(name)
        tracks = helpers.extract_tracks(data)
        tracks.to_json(writePath + os.path.relpath(name, readPath), orient='table')
