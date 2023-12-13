import osmnx as ox
import networkx as nx
import geopy.distance

# Function to calculate distance between two latitude, longitude points
def calculate_distance(coord1, coord2):
    return geopy.distance.distance(coord1, coord2).meters

# Function to calculate the shortest path distance between two points
def shortest_path_distance(lat1, lon1, lat2, lon2):
    # Create a graph from OpenStreetMap data
    G = ox.graph_from_point((lat1, lon1), distance=500, network_type='drive')

    # Get the nearest nodes to the specified coordinates
    origin_node = ox.get_nearest_node(G, (lat1, lon1))
    target_node = ox.get_nearest_node(G, (lat2, lon2))

    # Calculate the shortest path using Dijkstra's algorithm
    shortest_path = nx.shortest_path(G, origin_node, target_node, weight='length')

    # Calculate the total distance of the shortest path
    total_distance = sum(calculate_distance(G.nodes[u]['x'], G.nodes[v]['x']) for u, v in zip(shortest_path[:-1], shortest_path[1:]))

    return total_distance

# Example usage
lat1, lon1 = 0.3266102817436197, 32.562835434550394  # New York City
lat2, lon2 = 0.32245097708046744, 32.56206990609578 # Los Angeles

distance = shortest_path_distance(lat1, lon1, lat2, lon2)
print(f"The shortest path distance between the coordinates is: {distance:.2f} meters.")
