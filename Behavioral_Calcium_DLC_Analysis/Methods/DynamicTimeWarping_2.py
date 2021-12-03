# Author: Romain Tavenard
# License: BSD 3 clause

import matplotlib.pylab as plt
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import math

# conda install -c conda-forge tslearn
from tslearn import metrics
from sklearn.metrics import classification_report
import random

PLOT_SAVE_PATH = r"/Users/rodrigosandon/Documents/GitHub/LBGN/Figures/dtw_2.png"


def euclid_dist(t1, t2):
    return math.sqrt(sum((t1-t2)**2))

# s1 = time series 1
# s2 = time series 2

# every cell has it's series


def DTWDistance_1(s1, s2):
    DTW = {}

    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist = (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],
                                     DTW[(i, j-1)], DTW[(i-1, j-1)])

    return math.sqrt(DTW[len(s1)-1, len(s2)-1])


def DTWDistance_2(s1, s2, w):
    DTW = {}

    w = max(w, abs(len(s1)-len(s2)))

    for i in range(-1, len(s1)):
        for j in range(-1, len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist = (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],
                                     DTW[(i, j-1)], DTW[(i-1, j-1)])

    return math.sqrt(DTW[len(s1)-1, len(s2)-1])


def LB_Keogh(s1, s2, r):
    LB_sum = 0
    for ind, i in enumerate(s1):

        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])

        if i > upper_bound:
            LB_sum = LB_sum+(i-upper_bound)**2
        elif i < lower_bound:
            LB_sum = LB_sum+(i-lower_bound)**2

    return math.sqrt(LB_sum)


def knn(train, test, w):
    preds = []
    for ind, i in enumerate(test):
        min_dist = float('inf')
        closest_seq = []
        for j in train:
            if LB_Keogh(i[:-1], j[:-1], 5) < min_dist:
                dist = DTWDistance_2(i[:-1], j[:-1], w)
                if dist < min_dist:
                    min_dist = dist
                    closest_seq = j
        preds.append(closest_seq[-1])
    return classification_report(test[:, -1], preds)


def k_means_clust(data, num_clust, num_iter, w=5):
    centroids = random.sample(data, num_clust)
    counter = 0
    for n in range(num_iter):
        counter += 1
        print(counter)
        assignments = {}
        # assign data points to clusters
        for ind, i in enumerate(data):
            min_dist = float('inf')
            closest_clust = None
            for c_ind, j in enumerate(centroids):
                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = DTWDistance_2(i, j, w)
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = []

        # recalculate centroids of clusters
        for key in assignments:
            clust_sum = 0
            for k in assignments[key]:
                clust_sum = clust_sum+data[k]
            centroids[key] = [m/len(assignments[key]) for m in clust_sum]

    return centroids


"""train = np.genfromtxt('datasets/train.csv', delimiter='\t')
test = np.genfromtxt('datasets/test.csv', delimiter='\t')
print(knn(train, test, 4))"""


"""train = np.genfromtxt('datasets/train.csv', delimiter='\t')
test = np.genfromtxt('datasets/test.csv', delimiter='\t')
data = np.vstack((train[:, :-1], test[:, :-1]))


centroids = k_means_clust(data, 4, 10, 4)
for i in centroids:

    plt.plot(i)

plt.show()"""
