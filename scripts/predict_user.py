from supabase import create_client, Client
import os


url = 'https://uoyylajbuvbqfsavvqme.supabase.co' # Replace with your own Supabase URL
key = os.getenv("api_key_supabase") # Import your os key with the name api_key_supabase

supabase: Client = create_client(url, key)

TableToFetch = 'UserData' # Table to use from database


def get_mean_of_items():  # Get all user data ratings and get the means for each catid
    data = supabase.table(TableToFetch).select('username, catid, rating').execute().data
    catid_data = {}
    catid_count = {}

    for row in data:
        catid = row['catid']
        rating = row['rating']
        catid_data[catid] = catid_data.get(catid, 0) + rating
        catid_count[catid] = catid_count.get(catid, 0) + 1

    sorted_catid_data = {catid: catid_data[catid] / catid_count[catid] for catid in sorted(catid_data, key=lambda x: catid_data[x]/catid_count[x], reverse=True)}

    return sorted_catid_data

def get_mean_of_items_in_area(lat, long, item_in_area, api_key):
    all_items = get_mean_of_items()
    catid_list = []
    for catid in all_items.keys():
        if str(catid) in [item[0] for item in item_in_area]:
            catid_list.append(catid)
    top_rated_items_in_area = {catid: all_items[catid] for catid in catid_list if catid in all_items}
    return top_rated_items_in_area



def get_user_ratings(username):  # Query for the user ratings
    userdata = supabase.table(TableToFetch).select('username, catid, rating, count, sum').eq('username', username).execute()
    return userdata.data if userdata.data else []


def get_10_best_rated(username):  # Returns the users 10 best-rated categories
    userdata = get_user_ratings(username)
    if not userdata:
        return []
    userdata.sort(key=lambda x: x['rating'], reverse=True)
    return [row['catid'] for row in userdata[:10]]


def suggest_filterid(username, lat, long, item_in_area, api_key):
    filterid = []
    items = get_mean_of_items_in_area(lat, long, item_in_area, api_key)

    # sort items by rating in descending order
    sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)

    # retrieve the user's best-rated items
    user_items = set(get_10_best_rated(username))

    # add highly rated items that haven't been rated by the user
    for item in sorted_items:
        catid = item[0]
        if catid not in user_items and item[1] >= 3.0 and len(filterid) < 10:
            filterid.append(str(catid))

    # add the user's best-rated items if the list has not reached its maximum length
    for item in user_items:
        if item not in filterid and len(filterid) < 10:
            filterid.append(str(item))

    # sort the list in descending order of rating
    filterid.sort(key=lambda x: items[int(x)], reverse=True)

    return filterid


