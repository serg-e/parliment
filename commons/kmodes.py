import numpy as np
from scipy import stats

'''
K modes

Step 1: Randomly select k unique objects as the
initial cluster centers (modes).
Step 2: Calculate the distances between each
object and the cluster mode; assign the object to the
cluster whose center has the shortest distance to the
object; repeat this step until all objects are assigned
to clusters.
Step 3: Select a new mode for each cluster and
compare it with the previous mode. If different, go
back to Step 2; otherwise, stop.


'''


def distance(xi,q):
#     print(xi,'dist from',q)
    assert len(xi)==len(q),'Sequences of unequal length, distance undefined'
    dist = 0
    for i, j in zip(list(xi),list(q)):
        if i!=j:
            dist+=1
    return dist

def initlise_rand_modes(X,k):
    #initialise, ineefficient !
    unique_rows = np.unique(X, axis =0)
    rand = np.random.permutation(unique_rows)
    return rand[:k]


def assign_mode(xi,modes):
    '''needs work, if two modes equadistant the first one is picked'''
    dists = [distance(xi,q) for q in modes]
    # if len(dists) != len(set(dists)):
    #     print('xi',xi,'modes',modes)
    return dists.index(min(dists))
#     return np.concatenate(xi,[dists.index(min(dists))])

def assign_modes(X,modes):
    # 'vector assigning each xi to mode'
    cluster_vector = np.array([assign_mode(xi,modes) for xi in X])
    return cluster_vector

def calc_new_modes(X,cluster_vector,modes, verbose=False):
    new_modes = []
    for k, q in enumerate(modes):
        cluster = X[cluster_vector==k]
        if verbose: print('Cluster {0} is length {1}'.format(k, len(cluster)))
        try:
            new_mode = stats.mode(cluster)[0][0]
            new_modes.append(new_mode)

        except IndexError:
            # empty
            q = initlise_rand_modes(X,1)
            new_modes.append(q)

    return np.array(new_modes)



def kmodes(X,k, init_modes=None, verbose=True):
    ''' X data n x m_attr , k modes , output tuple of arrays
    (modes 1 x k , cluster vector 1xi)'''
    #red inti variables
    n, m_attr = X.shape

    if type(init_modes) == type(None):
        end_modes = initlise_rand_modes(X,k)
        print('Rand init')
    else:
        end_modes = init_modes
        print('Init modes provided')

    start_modes = np.ones_like(end_modes)
    #
    start_cluster_vector = np.ones(n)
    end_cluster_vector = np.random.randn(n)

    i = 0
    while not (end_cluster_vector == start_cluster_vector).all():
        # print('iter_start','END',end_modes,'START', start_modes)
        start_modes = end_modes
        start_cluster_vector = end_cluster_vector
        end_cluster_vector = assign_modes(X,start_modes)
        end_modes = calc_new_modes(X,end_cluster_vector, start_modes)

        # print('iter_end','END',end_modes,'START', start_modes)
        i+=1


    cluster_vector = assign_modes(X,end_modes)

    if verbose: print('{} iterations performed by kmodes'.format(i))

    return(end_modes, cluster_vector)


class Kmodes:

    def __init__(self, k_clusters, n_pools=1, distance=distance):
        self.k_clusters = k_clusters
        self.distance = distance
        self.n_pools = n_pools



    def fit(self,X):
        m_attr = X.shape[1]
        self.mode_pool = np.ones((self.k_clusters, m_attr))

        if self.n_pools == 1:
            self.modes, self.cluster_vector = kmodes(X, self.k_clusters)
            self.mode_pool = []
            return None

        self.mode_pool, _  = kmodes(X,self.k_clusters)

        for i in range(self.n_pools-1):
            end_modes, _  = kmodes(X,self.k_clusters)
            self.mode_pool = np.concatenate([self.mode_pool, end_modes])

        self.init_modes = np.ones_like(initlise_rand_modes(X,self.k_clusters))



        # self.modes, self.cluster_vector = kmodes(X, self.k_clusters,\
        # self.init_modes)




    def predict(X):
        pass

if __name__=='__main__':pass
