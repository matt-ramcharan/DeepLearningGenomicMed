#import shogun
import numpy as np
import binarytree
import scipy
from binarytree import build
import pandas as pd
from scipy.spatial.distance import euclidean, pdist, squareform
import matplotlib.pyplot as plt


def similarity_func(u, v):
    return 1/(1+euclidean(u,v))


def change_repres_rand(top,node,m):
    #top[node].pprint()
    subtree = top[node].values
    repres_index = np.random.choice(range(len(top[node].represN)), m, replace=False)
    for subnode in subtree:
        cur_rep = getattr(top[subnode], 'represN')
        new_rep = cur_rep
        for j in repres_index:
            new_rep[j] = cur_rep[j]*-1

        setattr(top[subnode], 'represN', new_rep)
        #print(getattr(top[subnode],'represN'))
        #print('\n')
    return top
def rand_change_recurse(root,m):
    order = root.preorder
    for node in order:
        root = change_repres_rand(root, node.value, m)
        #print([leav.represN for leav in root.leaves])
    return root


if __name__ == "__main__":

    # Build a tree from list representation

    #tree_size = 7
    tree_size = 64-1
    #repres_size = 5
    repres_size = 100


    values = range(0,tree_size)
    repres_orig = [[1]*repres_size] * tree_size
    root = build(values,repres=repres_orig.copy())
    #print(repres_orig)

    #m = 5
    m=1

    root.pprint()
    #root = change_repres_rand(root, 1, m)
    root = rand_change_recurse(root, m)

    #root.pprint()
    represes = [rep.represN for rep in root.leaves]
    #np.array(represes).T.tolist()
    labels = root.leaves

    DF_var = pd.DataFrame(represes)
    DF_var.index = labels

    dists = pdist(DF_var, similarity_func)
    DF_euclid = pd.DataFrame(squareform(dists))
    #print(DF_euclid)
    plt.matshow(DF_euclid.corr())
    plt.show()

    dist1 = np.random.normal()
