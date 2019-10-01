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

def initilise_rand_modes(X,k):
    #initialise, ineefficient !
    unique_rows = np.unique(X, axis =0)
    rand = np.random.permutation(unique_rows)
    return rand[:k]

def initialise_cao(X,k):
    # density based initilisation, Cao et al 2009
    # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.474.8181&rep=rep1&type=pdf


    n, m_attr = X.shape

    modes = []

    dens = np.zeros(n)

    # dens_a w.r.t. attribute a  = number of elements in U with matching attribute / n
    # dens = sum over dens w.r.t. a / m_attr

    for i in range(n):

        dens_a =[]

        for m in range(m_attr):
            attrs, counts = np.unique(X[:,m], return_counts=True)
            freq = {attr:count for attr, count in zip(attrs,counts)}
            dens_a.append(freq[X[i,m]]/float(n))

        dens[i] = sum(dens_a)/float(m_attr)


    modes.append(X[np.argmax(dens)])



    for i in range(1,k):
        scores = np.empty((len(modes),n))
        for k in range(len(modes)):
            scores[k] = dens*np.array([distance(i, modes[k]) for i in X])




        modes.append(X[np.argmax(np.min(scores,axis=0))])

    return np.array(modes)




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
            q = initilise_rand_modes(X,1)
            new_modes.append(q)

    return np.array(new_modes)



def kmodes(X,k, init, verbose=False):
    ''' X data n x m_attr , k modes , output tuple of arrays
    (modes 1 x k , cluster vector 1xi)'''
    #red inti variables
    n, m_attr = X.shape

    end_modes = init(X,k)

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

    def __init__(self, k_clusters, n_pools=1, distance=distance, init=initialise_cao):
        self.k_clusters = k_clusters
        self.distance = distance
        self.n_pools = n_pools
        self.init = init



    def fit(self,X):

        self.modes, self.cluster_vector = kmodes(X,self.k_clusters,init)


    def predict(X):
        assign_modes(X,self.modes)

if __name__=='__main__':pass
