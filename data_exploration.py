from start_db import Session
from mapped_classes import *
import pandas as pd
import numpy as np
from kmodes import kmodes


def make_mp_votes_array(mps, div_nums):
    ''' array : len(mps) x len(div_nums) sequence of votes fo reach mp (row)'''
    votes = [mp.votes for mp in mps]
    filtered_votes = [[vote.vote for vote in filter(lambda vote : vote.division_number in div_nums, mp)] for mp in votes]
    return np.array(filtered_votes)



if __name__ == '__main__':
    session = Session()
    mps = session.query(MP).all()
    divs = session.query(Division).all()
    div_nums = [div.division_number for div in divs]
    mp_votes_matrix = make_mp_votes_array(mps, div_nums)
    modes, cluster_map = kmodes(mp_votes_matrix,2)
    data = np.array([[mp.name for mp in mps],[mp.person_id for mp in mps], cluster_map,[mp.party for mp in mps]]).transpose()
    results = pd.DataFrame(data, columns=['name', 'id','cluster', 'party'])
    results['cluster'] = results.cluster.astype(int)
    results[(results.cluster==1)*(results.pary=='Conservative')]
    print(results.head())
