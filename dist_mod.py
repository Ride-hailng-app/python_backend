import numpy as np
from sklearn.neighbors import KDTree
# Example dataset with known coordinates (latitude and longitude)
dataset = np.array([
    [40.000, -74.0060],
    [100.0101, 10000.0001],
    # Add more points as needed
])
kdtree = KDTree(dataset)

# Example query pair of coordinates
query_latitude = 40.7128
query_longitude = -74.0060
query_point = np.array([[query_latitude, query_longitude]])

# Set the number of nearest neighbors you want to find (k)
k = 2

# Query the KDTree for the k-nearest neighbors
distances, indices = kdtree.query(query_point, k=k)

print(distances)
print(indices)