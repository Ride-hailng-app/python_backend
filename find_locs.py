import math

EARTH_RADIUS_KM = 6371.0  # Earth's radius in kilometers

def haversine_distance(lon1, lat1, lon2, lat2):
    # Convert latitude and longitude from degrees to radians
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    print(f"dlon: {dlon} and dlat {dlat}")
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS_KM * c

    return distance

def generate_nearby_locations(initial_lon, initial_lat, max_distance_km):
    nearby_locations = []

    for lon in range(-180, 181):
        for lat in range(-90, 91):
            distance = haversine_distance(initial_lon, initial_lat, lon, lat)
            print(f"distance: {distance}")
            input("press enter")
            if distance <= max_distance_km:
                nearby_locations.append((lon, lat))

    return nearby_locations

# Example usage
initial_longitude = 32.571746
initial_latitude = 0.321332
max_distance_km = 25.0

#nearby_locations = generate_nearby_locations(initial_longitude, initial_latitude, max_distance_km)
#print(nearby_locations)

il = 0.359942
il = 32.562494
