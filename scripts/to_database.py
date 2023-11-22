from supabase import create_client, Client
from . import predict_user as pu  # Importing predict_user module for additional functionality

url = '' # Replace with your own Supabase URL
key = '' # Replace with your own Supabase api_key

supabase: Client = create_client(url, key)

TableToFetch = 'UserData'  # Table to use from the database

def get_userdata(username):
    """
    Get user data, including ratings, for a given username.

    Args:
        username (str): The username for which to retrieve data.

    Returns:
        list: User data, including ratings.
    """
    userda = pu.get_user_ratings(username)
    return userda

def send_data(username, POIInfo, rating):
    """
    Update or insert user data for a given username and Point of Interest (POI) information.

    Args:
        username (str): The username for which to update or insert data.
        POIInfo (dict): Point of Interest information.
        rating (float): The rating to update or insert.

    Returns:
        None
    """
    for catid in POIInfo:
        userdata = get_userdata(username)
        itemExists = False

        for sublist in userdata:
            if sublist['catid'] == int(catid):
                itemExists = True
                rating_sum = float(sublist['sum']) + rating
                count = float(sublist['count']) + 1
                ratingVal = rating_sum / count
                update_data = {'sum': int(rating_sum), 'count': int(count), 'rating': ratingVal}
                supabase.table(TableToFetch).update(update_data).eq('username', username).eq('catid', catid).execute()

        if not itemExists:
            data = {'username': username, 'catid': catid, 'count': 1, 'rating': rating, 'sum': rating}
            supabase.table(TableToFetch).insert(data).execute()
