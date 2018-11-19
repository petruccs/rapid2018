import json
import pandas as pd
import numpy as np


def get_pv_params(track, mcps, mcvs):
    """ Given a track dict, the list of MCParticles and MCVertices return the
    track PV position and ID (or None if not found or ambiguous)
    """
    track_mcps = track['MCPs']
    # We ignore the tracks with no association to MCP or more than one
    if len(track_mcps) != 1:
        return None
    track_mcp = mcps[track_mcps[0]]
    track_pv_id = track_mcp['PV']
    track_pv = mcvs[track_pv_id]
    pos = track_pv['Pos']
    return pos[0], pos[1], pos[2], track_pv['key']


def load_data(filename, add_pv_params=True):
    """ Read tracks from a single json event into a dataframe
    """
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

    # add mc pv info to all tracks with minimum one particle hypothesis
    if add_pv_params:
        df['mcpx'] = df['mcpy'] = df['mcpz'] = df['mcpvid'] = np.nan
        for index, row in df.iterrows():
            df.loc[index, ['mcpx', 'mcpy', 'mcpz', 'mcpvid']] = get_pv_params(row, data['MCParticles'], data['MCVertices'])

    return df
