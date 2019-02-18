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

"""
def change_repres_rand(top,node,m):
    #print(top.represN)
    top[node].pprint()
    #top[node].represN = [1,1,1]
    subtree = top[node].levelorder
    for i in subtree:
        repres_index = np.random.choice(range(len(i.represN)), m, replace=False)
        for j in repres_index:
            cur_rep = getattr(i,'represN')
            new_rep = cur_rep
            new_rep[j] = cur_rep[j]*-1
            setattr(i,'represN',new_rep)

            #setattr(i,'value',100)

            print(getattr(i,'represN'))
        print('\n')
    return top
"""
def rand_change_recurse(root,m):
    order = root.preorder
    for node in order:
        root = change_repres_rand(node,m)
    return root


if __name__ == "__main__":

    # Build a tree from list representation

    tree_size = 7
    #tree_size = 64-1
    repres_size = 5
    #repres_size = 100


    values = range(0,tree_size)
    repres_orig = [[1]*repres_size] * tree_size
    root = build(values,repres=repres_orig.copy())
    print(repres_orig)

    m = 3

    root.pprint()

    node = 1
    root[node].pprint()
    #top[node].represN = [1,1,1]
    subtree = root[node].values

    for subnode in subtree:

        repres_index = np.random.choice(range(len(root[subnode].represN)), m, replace=False)
        cur_rep = getattr(root[subnode], 'represN')
        new_rep = cur_rep
        for j in repres_index:
            new_rep[j] = cur_rep[j]*-1

        setattr(root[subnode], 'represN', new_rep)
        print(getattr(root[subnode],'represN'))
        print('\n')


    print(repres_orig)
    root.pprint()
    represes = [rep.represN for rep in root.leaves]
    #np.array(represes).T.tolist()
    labels = root.leaves

    DF_var = pd.DataFrame(represes)
    DF_var.index = labels

    dists = pdist(DF_var, similarity_func)
    DF_euclid = pd.DataFrame(squareform(dists))
    print(DF_euclid)
    plt.matshow(DF_euclid.corr())
    plt.show()
