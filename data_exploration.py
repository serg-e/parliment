from start_db import Session
from mapped_classes import *
import pandas as pd
import numpy as np
from kmodes import kmodes
from sqlalchemy import inspect


def make_mp_votes_array(mps, div_nums):
    ''' array : len(mps) x len(div_nums) sequence of votes fo reach mp (row)
    input array for kmodes
    '''
    votes = [mp.votes for mp in mps]
    filtered_votes = [[vote.vote for vote in filter(lambda vote : vote.division_number in div_nums, mp)] for mp in votes]
    return np.array(filtered_votes)

def cluster_mps(mps,k,div_nums):
    ''' list of mps , number of clusters and divsions to cluster on, returns
    dataframe and array of cluster centres'''
    mp_votes_array = make_mp_votes_array(mps, div_nums)
    modes, cluster_map = kmodes(mp_votes_array,k)
    names = [mp.name for mp in mps]
    person_ids = [mp.person_id for mp in mps]
    party = [mp.party for mp in mps]
    data = np.array([names,person_ids, party, cluster_map]).transpose()
    results = pd.DataFrame(data, columns=['name', 'person_id', 'party', 'cluster'])
    results['cluster'] = results.cluster.astype(int)
    results['person_id'] = results.person_id.astype(int)

    return results, modes



if __name__ == '__main__':


    print(results.head())
