# Importing necessary modules and scripts
from flask import Flask, jsonify, json
import scripts.poi_filter as pfi
import scripts.poi_finder as pf
import scripts.route_generator as rg
import scripts.predict_user as pu
import scripts.to_database as TD
import urllib
import random
import os

# Initialize Flask application
api_key = os.getenv("api_key_ors")  # Replace this with your actual Openrouteservice API key
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return 'Hello, World!'

# Define a route for generating a route based on given parameters
@app.route('/GetRoute/<lat>/<long>/<profile>/<route_pois>/')
@app.route('/GetRoute/<lat>/<long>/<profile>/<route_pois>')
def send_array(lat, long, profile, route_pois):
    # Decode the URL-encoded route_pois parameter and load it as JSON
    route_pois = urllib.parse.unquote(route_pois, encoding='utf-8', errors='replace')
    pois = json.loads(route_pois)
    
    # Generate a route using the provided parameters
    route = rg.generate_route([long, lat], pois, profile, api_key)
    
    # Return the generated route as JSON
    return jsonify(route)

# Define a route for getting points of interest based on location and optional filter
@app.route('/GetPois/<lat>/<long>/')
@app.route('/GetPois/<lat>/<long>')
@app.route('/GetPois/<lat>/<long>/<filter>')
@app.route('/GetPois/<lat>/<long>/<filter>/')
def get_pois(lat, long, filter=None):
    # Get points of interest based on the provided location and radius
    Pois = pf.get_points_of_interest(float(lat), float(long), 2000, api_key)
    
    # Get additional information for each point of interest
    PoiInfo = pf.get_poi_info(Pois)
    
    # Check if a filter is provided, and filter the points of interest accordingly
    if filter is None or len(filter) == 0:
        return jsonify(PoiInfo)
    else: 
        filtered_id_list = pf.get_filter_id_list(Pois)
        return jsonify(pfi.filter_by_group_and_type(PoiInfo, filter, filtered_id_list))

# Define a route for getting a list of point of interest IDs based on location
@app.route('/GetIdList/<lat>/<long>/')
@app.route('/GetIdList/<lat>/<long>')
def Get_Id_list(lat, long):
    # Get points of interest based on the provided location and radius
    Pois = pf.get_points_of_interest(float(lat), float(long), 2000, api_key)
    
    # Return a list of point of interest IDs
    return jsonify(pf.get_filter_id_list(Pois))

# Define a route for getting a random list of point of interest IDs based on location
@app.route('/GetRandomIdList/<username>/<lat>/<long>')
@app.route('/GetRandomIdList/<username>/<lat>/<long>/')
def Get_Random_Id_list(username, lat, long):
    # Get points of interest based on the provided location and radius
    Pois = pf.get_points_of_interest(float(lat), float(long), 2000, api_key)
    
    # Get a random list of point of interest IDs
    item_in_area = pf.get_filter_id_list(Pois)
    return jsonify(pu.suggest_filterid(username, lat, long, item_in_area, api_key))

# Define a route for sending user ratings to the database
@app.route('/SendRating/<username>/<catids>/<rating>')
@app.route('/SendRating/<username>/<catids>/<rating>/')
def send_to_database(username, catids, rating):
    try:
        # Split the comma-separated category IDs and send data to the database
        catids_list = catids.split(",")
        TD.send_data(username, catids_list, int(rating))
        return '', 200
    except Exception as e:
        # Return an error message in case of an exception
        return {'error': str(e)}, 500
