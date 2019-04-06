import numpy as np

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
    dist = 0
    for i, j in zip(list(xi),list(q)):
        if i!=j:
            dist+=1
    return dist

def initlise_modes(X,k):
    #initialise
    modes =[]
    init_modes= np.random.choice(list(range(len(X))),size=k)
    for i in init_modes:
        modes.append(X[i])
    return np.array(modes)

def assign_mode(xi,modes):
    '''needs work, if two modes equadistant the first one is picked'''
    dists = [distance(xi,q) for q in modes]
    return dists.index(min(dists))
#     return np.concatenate(xi,[dists.index(min(dists))])

def assign_modes(X,modes):
    'vector assigning each xi to mode'
    cluster_vector = np.array([assign_mode(i,modes) for i in X])
    return cluster_vector

def calc_new_modes(X,cluster_vector,modes):
    new_modes = []
    for k, q in enumerate(modes):
        cluster = X[cluster_vector==k]
#         print(k, cluster)
        try:
            new_mode = stats.mode(cluster)[0][0]
            new_modes.append(new_mode)
        except:
            return modes
    return np.array(new_modes)


def kmodes(X,k):
    end_modes = initlise_modes(X,2)
    start_modes = np.ones_like(end_modes)
    
    while not (end_modes == start_modes).all():
#         print('iter_start','END',end_modes,'START', start_modes)
        start_modes = end_modes
        cluster_vector = assign_modes(X,start_modes)
        end_modes = calc_new_modes(X,cluster_vector, start_modes)
    
    cluster_vector = assign_modes(X,end_modes)
    
    return(end_modes, cluster_vector, )
