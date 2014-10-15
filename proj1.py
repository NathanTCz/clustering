import sys
import random
import string

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

def cluster_points (dataset, centers):
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

  for key, center in zip(keys, centers):
    if key == str(center):
      for vector in clusters[key]:
        distance = 0
        for v, c in zip(vector, center):
          distance += ( (v - c)**2 )
    km_cost += distance

  return km_cost

fname = sys.argv[1]
k_clusters = int(sys.argv[2])
cluster_alg = str(sys.argv[3])
dataset = []

# Read in data
with open( fname, 'r' ) as f:
  for line in f:
    save = []
    cur_line = line.split()
    for num in cur_line:
      save.append( float(num) )
      dataset.append(save);

if cluster_alg == 'kmeans':
  best_kmcost = float("inf")
  best_clusters = {}

  for n in range(100):
    old_centers = []
    centers = random.sample( dataset, k_clusters )
    #centers = [[2.7], [1.7], [3.0]]

    while not centers == old_centers:
      old_centers = centers
      clusters = cluster_points(dataset, centers)

      # Recalculate centers
      centers = recalc_centers(clusters)

    # Calcualte K-means cost
    km_cost = kmeans_cost(clusters, centers)
    if (km_cost < best_kmcost):
      best_kmcost = km_cost
      best_clusters = clusters

  # Print clustering assignments
  print(best_kmcost)

  clustering = [];
  for d in dataset:
    for c_num, c in enumerate(best_clusters.values()):
      if d in c:
        clustering.append(c_num)
  print('A = [', end='')
  print(*clustering, sep=',', end='')
  print(']')
