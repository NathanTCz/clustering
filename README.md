ASSIGNMENT #3 - Clustering Implementation
Author: Nathan Cazell
Date: 10/19/2014

This python script implements the Lloyds method or K-Means and
Average Linkage Hierarchical clustering algorithms.

REQUIREMENTS:
  - Python 3.x
  - matplotlib (required only for 2D/3D visualization)
  - Python Libraries:
    * sys
    * random
    * string
    * time
      Note: these libraries should be available by default and
            should not require and extra installation.

USE:
  python3 proj1.py <DATASET> <#CLUSTERS> <ALGORITHM>

  <DATASET>
    This can be a space delimited or tab delimited file of
    data points
  <#CLUSTERS>
    The number of cluster desired
  <ALGORITHM>
    'kmeans' or 'average'


2D/3D VISUALS:
  When Lloyds method is used the centroids are shown. They are
  displayed as the larger points with matching color of cluster.

  NOTE: If the colors in different clusters look the same, they are
        not. They are just very similar shades. This is due to random
        infinite color generation. Simply run the program again to
        get better, more significant color generations.
