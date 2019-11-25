import networkx as nx
import numpy as np
import pandas as pd
import sys

from networkx.algorithms import bipartite
from random import shuffle
from sklearn.cluster import SpectralClustering

FILENAME = '/om2/user/annakoop/DiabetesPredictionModel/dataset_diabetes/diabetic_data.csv'
TEST_FRACTION = 0.1
NETWORK_SIZE = 5000
N_CLUSTERS = 3

'''
Removes encounters such that each patient has maximum one encounter

If a patient has multiple encounters, an encounter with remission in <30 or >30
days is kept (randomly selected, if possible) because those will correspond to the
earlier encounters.
'''
def remove_duplicate_patients(data):
    data_dict = {}
    for row in data:
        if row[1] in data_dict:
            data_dict[row[1]].append(row)
        else:
            data_dict[row[1]] = [row]
    data_pruned = []
    for patient in data_dict:
        if len(data_dict[patient]) == 1:
            data_pruned.append(data_dict[patient][0])
        else:
            options = []
            for encounter in data_dict[patient]:
                if encounter[49] == '<30' or encounter[49] == '>30':
                    options.append(encounter)
            if len(options) == 0:
                options = data_dict[patient]
            ind = np.random.randint(0, len(options))
            data_pruned.append(options[ind])
    return data_pruned

'''
Separates data into test and train sets with fraction TEST_FRACTION
'''
def separate_test_train(data):
    shuffle(data)
    cutoff = int(len(data) * (1 - TEST_FRACTION))
    return data[:cutoff], data[cutoff:]

'''
Makes an adjacency matrix based on similar medicines
'''
def make_network(data):
    # to insure all nodes are connected, initialize with ones
    adj = np.ones((len(data), len(data)), dtype=np.int8)
    for x, row1 in enumerate(data):
        for y, row2 in enumerate(data[x + 1:]):
            # medications span indices 24 - 46
            for i in range(24, 47):
                if row1[i] == row2[i] and row1[i] != 'No':
                    adj[x, y] += 1 
        if x % 200 == 0:
            print(x)
    return adj

def print_stats(group, name):
    meds = [0 for i in range(24)]
    res = {'<30': 0, '>30': 0, 'NO': 0}
    for row in group:
        for i in range(24, 47):
            if row[i] != 'No':
                meds[i] += 1
        res[i[49]] += 1
    print('%s stats' % name)
    print('meds: ', meds)
    print('res: ', res)
    
# '''
# Use spectral clustering to divide network into two groups
# '''
# def spectral_clustering(graph):
#     res = bipartite.spectral_bipartivity(graph)
#     print(res)
#     group_1 = set()
#     group_2 = set()
#     for node in res:
#         if res[node] > 0:
#             group_1.add(node)
#         else:
#             group_2.add(node)
#     print_stats(group_1, 'group 1')
#     print_stats(group_1, 'group 1')
#     return group_1, group_2

def analyze_clusters(data, labels):
    cluster_sizes = [0]*N_CLUSTERS
    readmission_frac = [0]*N_CLUSTERS
    meds_frac = [[0 for i in range(23)] for j in range(N_CLUSTERS)]
    for i, row in enumerate(data):
        c = labels[i]
        cluster_sizes[c] += 1
        if row[49] == '<30' or row[49] == '>30':
            readmission_frac[c] += 1
        for m in range(24, 47):
            if row[m] != 'No':
                meds_frac[c][m - 24] += 1
    print('cluster sizes: ', cluster_sizes)
    readmission_frac = [readmission_frac[i]/cluster_sizes[i] for i in range(N_CLUSTERS)]
    print('readmission fraction by cluster: ', readmission_frac)
    for i in range(N_CLUSTERS):
        meds_frac[i] = [meds_frac[i][j] / cluster_sizes[i] for j in range(23)]
    print('meds fraction by cluster: ', meds_frac)
        

def main():
    print('reading data from file...')
    data = pd.read_csv(FILENAME).to_numpy()
    
    print('organizing the data set...')
    data_clean = remove_duplicate_patients(data)
    train_data, test_data = separate_test_train(data_clean)
    print('train dataset size: %d' % len(train_data))
    print('test dataset size: %d' % len(test_data))
    
    print('making network...')
    adj = make_network(data[:NETWORK_SIZE])

    print('spectral clustering...')
    clustering = SpectralClustering(n_clusters=N_CLUSTERS).fit(adj)
    
    print('analyzing clusters...')
    analyze_clusters(data[:NETWORK_SIZE], clustering.labels_)
    

if __name__ == '__main__':
    main()