# ------- K-MEANS AND AVERAGE LINKAGE CLUSTERING --------
# COMMAND LINE INPUT:
#   1. Data File: tab delimited excel file or space delimited
#      values
#   2. K: specifically the number of desired clusters
#   3. Algorithm: 'kmeans' or 'average'
# DESCRIPTION:
#   This python script aims to implement Lloyds Method clustering
#   and Average linkage clustering.

import sys
import random
import string
import time
import numpy as np

# Determine if 2D visualisation libraray is present
twoD_supported = True
try:
  import matplotlib.pyplot as plt
except ImportError:
  print('Python Library: \'matplotlib\' missing, 2D visualisation not supported')
  twoD_supported = False

threeD_supported = True
try:
  from mpl_toolkits.mplot3d import Axes3D
except ImportError:
  print('Python Library: \'mpl_toolkits\' missing, 3D visualisation not supported')
  threeD_supported = False

# START - GENERIC FUNCTIONS
def find_in_cluster (point, clusters):
  for c_num, key in enumerate( sorted(clusters) ):
    if point in clusters[key]:
      return c_num

def get_clusterings (dataset, clusters):
  clustering = []
  for d in dataset:
    clustering.append( find_in_cluster(d, clusters) )

  return clustering

fname = sys.argv[1]
k_clusters = int(sys.argv[2])
cluster_alg = str(sys.argv[3])
dataset = []

# Read in data
# FORMAT:
#   - EX. Lines in a 3 dimesion data file look like:
#     1.0 2.0 3.0
#     4.0 5.0 6.0
#   These lines are parsed line by line as a two dimensional
#   list:
#     dataset = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
with open( fname, 'r' ) as f:
  for line in f:
    save = []
    cur_line = line.split()
    for num in cur_line:
      save.append( float(num) )
    dataset.append(save);

# ----------------- K-MEANS CLUSTERING --------------------
# Inital centers are randomly chosen from the given data
# points. distances between centers and points are calculated
# and the points are clustered with the center that is the
# shortest distance away. Centers are then recalculated based
# the average of all the points in that cluster. The algorithm
# stops on convergence, namely when the centers remain the same
# for two consecutive iterations.

def calc_closest (vector, centers):
  closest_dist = float("inf")
  closest_center = []

  for center in centers:
    distance = 0
    for v, c in zip(vector, center):
      distance += ( (v - c)**2 )
    distance = distance**(0.5)

    if distance < closest_dist:
      closest_dist = distance
      closest_center = center

  return str(closest_center)

def clusterize (dataset, centers):
  clusters  = {}
  for d in dataset:
    closest_center = calc_closest(d, centers)

    try:
      clusters[closest_center].append(d)
    except KeyError:
      clusters[closest_center] = [d]

  return clusters

def recalc_centers (clusters):
  labels = sorted( clusters.keys() )
  new_centers = []
  for l in labels:
    mean = [float(sum(col))/len(col) for col in zip(*clusters[l])]
    new_centers.append(mean)

  return new_centers

def kmeans_cost (clusters, centers):
  km_cost = float(0)
  keys = sorted( clusters.keys() )
  centers = sorted(centers)
  distance = 0

  for key, center in zip(keys, centers):
    if key == str(center):
      for vector in clusters[key]:
        distance = 0
        for v, c in zip(vector, center):
          distance += ( (v - c)**2 )
        km_cost += distance

  return km_cost

def lloyds_method (dataset):
  best_kmcost = float("inf")
  best_clusters = {}
  best_centers = []

  for n in range(100):
    old_centers = []
    centers = random.sample( dataset, k_clusters )

    while not centers == old_centers:
      old_centers = centers
      clusters = clusterize(dataset, centers)

      # Recalculate centers
      centers = recalc_centers(clusters)

    # Calcualte K-means cost
    km_cost = kmeans_cost(clusters, centers)
    if (km_cost < best_kmcost):
      best_kmcost = km_cost
      best_clusters = clusters
      best_centers = centers

  return (best_kmcost, best_clusters, best_centers)

if cluster_alg == 'kmeans':
  start_time = time.time()

  kmcost, clusters, centers = lloyds_method(dataset)

  run_time = time.time() - start_time

  # Print clustering assignments
  print('running-time: ', run_time)
  print('k-means cost: ', kmcost)

  clustering = get_clusterings(dataset, clusters)

  print('A = [', end='')
  print(*clustering, sep=',', end='')
  print(']')

  # ---- 2D Color Coded Scatter Plot -----
  # only print if using 2 dimensional data
  if len( dataset[0] ) == 2 and twoD_supported:
    # generate random colors for each cluster
    colors = {}
    for c_num, c in enumerate( sorted(centers) ):
      colors[c_num] = np.random.rand( 4 )  # because its an RGBA value

    for d in dataset:
      x = d[0]
      y = d[1]
      color = colors[ find_in_cluster (d, clusters) ]

      plt.scatter(x, y, s=80, c=color, alpha=0.8)
    
    for key, c in enumerate( sorted(centers) ):
      x = c[0]
      y = c[1]
      color = colors[key]

      plt.scatter(x, y, s=240, c=color, alpha=0.8)
    plt.show()

  # ---- 3D Color Coded Scatter Plot -----
  # only print if using 3 dimensional data
  if len( dataset[0] ) == 3 and twoD_supported and threeD_supported:
    # generate random colors for each cluster
    colors = {}
    for c_num, c in enumerate( sorted(centers) ):
      colors[c_num] = np.random.rand( 4 ) # because its an RGBA value

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for d in dataset:
      x = d[0]
      y = d[1]
      z = d[2]
      color = colors[ find_in_cluster (d, clusters) ]

      ax.scatter(x, y, z, s=40, c=color, alpha=0.8)

    for key, c in enumerate( sorted(centers) ):
      x = c[0]
      y = c[1]
      z = c[2]
      color = colors[key]

      ax.scatter(x, y, z, s=160, c=color, alpha=0.8)
    plt.show()

# ------------------ AVERAGE LINKAGE CLUSTERING ------------------
# Each point starts as its own cluster. The cluster are then merged
# based on the shortest average between cluster distance. This distance
# is calculated by calculating the between cluster distance for each
# point in the cluster and then averaging those distances. The closest
# clusters are then merged.

def hierchical_cluster (clusters):
  # Find the two most similar points
  closest_dist = float("inf")
  merge_cluster = []
  start_time = time.time()

  for c1 in sorted(clusters.values()):
    for c2 in sorted(clusters.values()):
      dist = float(0.0)
      if not c1 == c2:
        for p1 in c1:
          for p2 in c2:
            tmp = float(0.0)
            for n1, n2 in zip(p1, p2):
              tmp += (n1 - n2)**2
            dist += tmp**(0.5)
        dist = dist / ( len(c1)*len(c2) )
        if dist < closest_dist:
          closest_dist = dist
          merge_cluster = c1 + c2
          pop_keys = []
          pop_keys.append( str(c1)[1:-1] )
          pop_keys.append( str(c2)[1:-1] )

  for key in pop_keys:
    clusters.pop( str(key) )
  clusters[ str(merge_cluster)[1:-1] ] = merge_cluster

  return clusters

def init_avg_clust (data):
  clusters = {}

  for d in data:
    clusters[ str(d) ] = [d]

  return clusters

def average_linkage (dataset):
  num_clust = len(dataset)
  while not num_clust == k_clusters:
    # init n clusters on first iteration
    if num_clust == len(dataset):
      clusters = init_avg_clust(dataset)

    clusters = hierchical_cluster(clusters)
    num_clust = len(clusters)
  return clusters

if cluster_alg == 'average':
  start_time = time.time()

  clusters = average_linkage(dataset)

  run_time = time.time() - start_time

  print('running-time: ', run_time)

  clustering = get_clusterings(dataset, clusters)

  print('A = [', end='')
  print(*clustering, sep=',', end='')
  print(']')

  # ---- 2D Color Coded Scatter Plot -----
  # only print if using 2 dimensional data
  if len( dataset[0] ) == 2 and twoD_supported:
    # generate random colors for each cluster
    colors = {}
    for c_num, c in enumerate(clusters.keys()):
      colors[c_num] = np.random.rand( 4 )  # because its an RGBA value

    for d in dataset:
      x = d[0]
      y = d[1]
      color = colors[ find_in_cluster (d, clusters) ]

      plt.scatter(x, y, s=80, c=color, alpha=0.8)
    plt.show()

  # ---- 3D Color Coded Scatter Plot -----
  # only print if using 3 dimensional data
  if len( dataset[0] ) == 3 and twoD_supported and threeD_supported:
    # generate random colors for each cluster
    colors = {}
    for c_num, c in enumerate(clusters.keys()):
      colors[c_num] = np.random.rand( 4 ) # because its an RGBA value

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for d in dataset:
      x = d[0]
      y = d[1]
      z = d[2]
      color = colors[ find_in_cluster (d, clusters) ]

      ax.scatter(x, y, z, s=40, c=color, alpha=0.8)
    plt.show()

# ------------------- HAMMING DISTANCE -------------------------
# The hamming distance between two clusterings is the number of
# positions where each clustering differs.
def hamming_dist (c1, c2, n):
  dist = float(0.0)

  for i in range(n):
    for j in range(i, n):
      if ( (c1[i] != c1[j] and c2[i] == c2[j]) or (c1[i] == c1[j] and c2[i] != c2[j]) ):
        dist += 1.0

  n = float(n)
  dist = dist / ( n * (n-1) / 2 )

  return dist

if cluster_alg == 'hamming':
  average_clusters = average_linkage(dataset)
  kmcost, lloyds_clusters, centers = lloyds_method(dataset)

  lloyds_clustering = get_clusterings(dataset, lloyds_clusters)
  average_clustering = get_clusterings(dataset, average_clusters)

  print('average: A = [', end='')
  print(*average_clustering, sep=',', end='')
  print(']')

  print('kmeans:  A = [', end='')
  print(*lloyds_clustering, sep=',', end='')
  print(']')

  dist = hamming_dist(average_clustering, lloyds_clustering, len(dataset))

  print('hamming-dist: ', dist)
