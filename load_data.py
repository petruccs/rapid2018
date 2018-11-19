import json
import pandas as pd

def load_data(filename):
    with open(filename) as jsonfile:
      data = json.load(jsonfile)
    df = pd.DataFrame(data['VeloTracks']).T
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
    df['event'] = data['EventNumber']
    df['run'] = data['RunNumber']
    df = df.drop('ClosestToBeam', axis=1).drop('errCTBState', axis=1)
    return df
