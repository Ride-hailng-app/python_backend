import math,numpy
from scipy.spatial import KDTree


def find_nearest_coordinates_kdtree(target, coordinates_list,id_list, k=10):
    kdtree = KDTree(coordinates_list)
    distances, indices = kdtree.query(target, k=k)
    nearest_coordinates = list()
    if isinstance(indices,numpy.ndarray):
        for i in indices:
            nearest_dic = dict()
            print(i)
            nearest_dic["coords"] = coordinates_list[i]
            nearest_dic["id"] = id_list[i]
            nearest_coordinates.append(nearest_dic)
    else:
        nearest_dic = dict()
        nearest_dic["coords"] = coordinates_list[indices]
        nearest_dic["id"] = id_list[indices]
        nearest_coordinates.append(nearest_dic)
    return nearest_coordinates

def move_point_north(latitude_deg, longitude_deg, distance_km):
    # Convert latitude and longitude from degrees to radians
    latitude_rad = math.radians(latitude_deg)
    longitude_rad = math.radians(longitude_deg)

    # Earth's radius in kilometers
    earth_radius_km = 6371.0

    # Convert distance_km to radians
    distance_rad = distance_km / earth_radius_km

    # Calculate the change in latitude
    delta_latitude_rad = distance_rad

    # Calculate the new latitude
    new_latitude_rad = latitude_rad + delta_latitude_rad

    # Calculate the new longitude
    new_longitude_rad = longitude_rad

    # Convert the new latitude and longitude back to degrees
    new_latitude_deg = math.degrees(new_latitude_rad)
    new_longitude_deg = math.degrees(new_longitude_rad)

    return new_latitude_deg, new_longitude_deg

def move_point_south(latitude_deg, longitude_deg, distance_km):
    # Convert latitude and longitude from degrees to radians
    latitude_rad = math.radians(latitude_deg)
    longitude_rad = math.radians(longitude_deg)

    # Earth's radius in kilometers
    earth_radius_km = 6371.0

    # Convert distance_km to radians
    distance_rad = distance_km / earth_radius_km

    # Calculate the new latitude
    new_latitude_rad = latitude_rad - distance_rad

    # Calculate the new longitude
    new_longitude_rad = longitude_rad

    # Convert the new latitude and longitude back to degrees
    new_latitude_deg = math.degrees(new_latitude_rad)
    new_longitude_deg = math.degrees(new_longitude_rad)

    return new_latitude_deg, new_longitude_deg

def move_point_west(latitude_deg, longitude_deg, distance_km):
    # Convert latitude and longitude from degrees to radians
    latitude_rad = math.radians(latitude_deg)
    longitude_rad = math.radians(longitude_deg)

    # Earth's radius in kilometers
    earth_radius_km = 6371.0

    # Convert distance_km to radians
    distance_rad = distance_km / earth_radius_km

    # Calculate the new latitude
    new_latitude_rad = latitude_rad

    # Calculate the change in longitude
    delta_longitude_rad = distance_rad / math.cos(latitude_rad)

    # Calculate the new longitude
    new_longitude_rad = longitude_rad - delta_longitude_rad

    # Convert the new latitude and longitude back to degrees
    new_latitude_deg = math.degrees(new_latitude_rad)
    new_longitude_deg = math.degrees(new_longitude_rad)

    return new_latitude_deg, new_longitude_deg

def move_point_east(latitude_deg, longitude_deg, distance_km):
    # Convert latitude and longitude from degrees to radians
    latitude_rad = math.radians(latitude_deg)
    longitude_rad = math.radians(longitude_deg)

    # Earth's radius in kilometers
    earth_radius_km = 6371.0

    # Convert distance_km to radians
    distance_rad = distance_km / earth_radius_km

    # Calculate the new latitude
    new_latitude_rad = latitude_rad

    # Calculate the change in longitude
    delta_longitude_rad = distance_rad / math.cos(latitude_rad)

    # Calculate the new longitude
    new_longitude_rad = longitude_rad + delta_longitude_rad

    # Convert the new latitude and longitude back to degrees
    new_latitude_deg = math.degrees(new_latitude_rad)
    new_longitude_deg = math.degrees(new_longitude_rad)

    return new_latitude_deg, new_longitude_deg