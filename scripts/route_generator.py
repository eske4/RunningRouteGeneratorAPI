import openrouteservice as ors
import pprint

def generate_route(start_location, poi_info_list, profile, api_key):
    """
    Generates a walking route using OpenRouteService API based on a list of POIs and a starting location.

    Args:
        start_location (tuple): A tuple of the form (longitude, latitude) representing the starting location.
        poi_info_list (list): A list of POIs to visit, where each POI is a tuple of the form (name, poi_type, coordinates).
        api_key (str): An API key to access the OpenRouteService API.

    Returns:
        A dictionary containing the route information in GeoJSON format.
    """
    client = ors.Client(key=api_key)
    coordinates = [start_location]
    coordinates += [[poi[2], poi[3]] for poi in poi_info_list]
    return client.directions(coordinates=coordinates,
                             profile=profile,
                             format='geojson')


def get_distance(route_geojson):
    """
    Gets the distance of a walking route in kilometers.

    Args:
        route_geojson (dict): A dictionary containing the route information in GeoJSON format.

    Returns:
        The distance of the walking route in kilometers as a float.
    """
    distance = route_geojson['features'][0]['properties']['segments'][0]['distance']
    return distance
    
def print_distance(distance):
    """
    Prints the distance in km

    Args:
        float: meters of route
    """
    print(f"Route distance: {distance/1000:.2f} km")
