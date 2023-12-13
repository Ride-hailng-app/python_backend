from scipy.spatial import KDTree
import numpy

def find_nearest_coordinates_kdtree(target, coordinates_list, k=5):
    kdtree = KDTree(coordinates_list)
    distances, indices = kdtree.query(target, k=k)
    nearest_coordinates = list()

    if isinstance(indices,numpy.ndarray):
        print("it's list")
    else:
        print("it's not list")
        
    for i in indices:
        print(i)
        nearest_coordinates.append([coordinates_list[i]])
    return nearest_coordinates

# Example usage:
target_coordinate = (6, 1)
coordinates_list = [(1, 2), (4, 8), (7, 1), (2, 6), (5, 5), (6, 3)]
nearest_5_coordinates = find_nearest_coordinates_kdtree(target_coordinate, coordinates_list)
print(nearest_5_coordinates)





