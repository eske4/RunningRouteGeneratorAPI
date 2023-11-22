import openrouteservice as ors
import pprint


def get_points_of_interest(latitude, longitude, buffer_radius, api_key):
    """
    Returns points of interest (POIs) within a given buffer radius from the specified latitude and longitude coordinates.

    Parameters:
    latitude (float): Latitude of the center point to search for POIs.
    longitude (float): Longitude of the center point to search for POIs.
    buffer_radius (int): The radius (in meters) around the center point within which to search for POIs.
    api_key (str): The API key to use for OpenRouteService.

    Returns:
    dict: A dictionary containing information about the POIs that were found.
    """
    client = ors.Client(key=api_key)
    geojson = {"type": "point", "coordinates": [longitude, latitude]}
    
    pois = client.places(request='pois',
                         geojson=geojson,
                         buffer=buffer_radius)
    
    return pois



def get_poi_info(pois):
    """
    Returns information about the POIs found in the specified dictionary.

    Parameters:
    pois (dict): A dictionary containing information about the POIs.

    Returns:
    list: A list containing information about the POIs in the format [name, poi_type, coordinates].
    """
    
    poi_info = []   

    for poi in pois['features']:
        osm = poi["properties"].get("osm_tags", {})
        if osm and osm.get("name"):
            name = osm["name"]
            poi_type = list(poi["properties"]["category_ids"].keys())[0]
            coordinates = poi["geometry"]["coordinates"]
            poi_info.append([name, poi_type, str(coordinates[0]), str(coordinates[1])])
            
    return poi_info


def get_filter_id_list(pois):
    """
    Returns a dictionary containing the filter IDs for the POIs found in the specified dictionary.

    Parameters:
    pois (dict): A dictionary containing information about the POIs.

    Returns:
    dict: A dictionary containing the filter IDs for the POIs in the format {poi_type: [category_group, category_name]}.
    """
    
    filter_id_list = []

    for poi in pois['features']:
        osm = poi["properties"].get("osm_tags", {})
        if osm and osm.get("name"):
            cat = poi["properties"]["category_ids"]
            poi_type = list(cat.keys())[0]
            line = [poi_type, cat[str(poi_type)]["category_group"], cat[str(poi_type)]["category_name"]]
            if line not in filter_id_list:
                filter_id_list.append(line)

            # filter_id_list[poi_type] = [cat[str(poi_type)]["category_group"], cat[str(poi_type)]["category_name"]]
    return filter_id_list
