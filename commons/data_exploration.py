from commons.db import Session
from commons.mapped_classes import *
from commons.kmodes import Kmodes
import pandas as pd
import numpy as np
from sqlalchemy import inspect
import os

eu_divisions = [357, 358, 359,360,361,362,373,374,375,377,378,394, 395, 404, \
                405,406,407,408,409,413,356,354,293,293,292,291,274]

def make_mp_votes_frame(mps, div_nums):
    ''' array : len(mps) x len(div_nums) sequence of votes fo reach mp (row)
    input array for kmodes
    '''
    # votes = np.empty((m, n), dtype=np.string_ )
    # inneficient! vectorise the loops and reduce copying

    votes = {mp.name: {} for mp in mps}

    for mp in mps:
        for div in div_nums:

            try:
                votes[mp.name][div] = list(filter(lambda vote: vote.division_number == div, mp.votes))[0].vote

            except IndexError:
                votes[mp.name][div] = 'absent'


    votes = pd.DataFrame(data=votes).transpose()

    return votes





def cluster_mps(mps,k,div_nums, n_pools=50):
    ''' list of mps , number of clusters and divsions to cluster on, returns
    dataframe and array of cluster centres'''
    mp_votes_array = make_mp_votes_frame(mps, div_nums)
    kmodes = Kmodes(k,n_pools)
    kmodes.fit(mp_votes_array)
    modes, cluster_map = kmodes.centroids , kmodes.cluster_vector
    names = [mp.name for mp in mps]
    person_ids = [mp.person_id for mp in mps]
    party = [mp.party for mp in mps]
    data = np.array([names,person_ids, party, cluster_map]).transpose()
    results = pd.DataFrame(data, columns=['name', 'person_id', 'party', 'cluster'])
    results['cluster'] = results.cluster.astype(int)
    results['person_id'] = results.person_id.astype(int)
    results.sort_values("party",inplace=True)
    return results, modes





def add_master_nodes(frame):
    clusters = set(frame.cluster)
    new_nodes = [{'person_id':'commons'}]
    for i in clusters:
        c = {'person_id':i, 'cluster':'commons'}
        new_nodes.append(c)
    frame = frame.append(new_nodes)
    return frame, new_nodes




def div2dict(div):
    div_dict = {'title': div.title , 'division_number':div.division_number,\
     'ayes':len(div.ayes), 'noes':len(div.noes), 'abstentions':len(div.abstentions)}
    return div_dict

def query2df(query):
    return pd.read_sql(query.statement, query.session.bind)




if __name__ == '__main__':
    session = Session()
    mps = session.query(MP).all()



    frame, _ = cluster_mps(mps,4,eu_divisions)
    nodes_frame =  add_master_nodes(frame)
    filename = 'web-app/mp_clusters.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as file:
        nodes_frame.to_json(file, orient='records')
