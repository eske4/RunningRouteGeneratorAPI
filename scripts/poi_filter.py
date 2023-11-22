# def filter_by_type(poi_list, poi_types):
#     """
#     Filters a list of points of interest (POIs) `poi_list` by POI type, returning only POIs that match the specified types.

#     Args:
#         poi_list (list): A list of POIs to filter.
#         poi_types (list): A list of POI types to filter by.

#     Returns:
#         A list of POIs from `poi_list` that match one or more of the POI types in `poi_types`.
#     """
#     def poi_type_filter(poi):
#         return poi[1] in poi_types
#     return list(filter(poi_type_filter, poi_list))

# def filter_by_group(poi_list, groups, filtered_id_list):
#     """
#     Filters a list of points of interest (POIs) `poi_list` by group, returning only POIs that match the specified groups.

#     Args:
#         poi_list (list): A list of POIs to filter.
#         groups (list): A list of groups to filter by.
#         filtered_id_list (dict): A dictionary of filtered POI IDs keyed by POI type ID.

#     Returns:
#         A list of POIs from `poi_list` that match one or more of the groups in `groups`.
#     """
#     def group_filter(poi):
#         poi_type_id = poi[1]
#         filtered_id = filtered_id_list[poi_type_id][0]
#         return filtered_id in groups
#     return list(filter(group_filter, poi_list))

def filter_by_group_and_type(poi_list, groups_and_types, filtered_id_list):
    def group_or_type_filter(poi):
        poi_type_id = poi[1]
        #if not isinstance(poi_type_id, int):
        #filtered_id = filtered_id_list[poi_type_id][1]
        filtered_id = ""
        for line in filtered_id_list:
            if line[0] == str(poi_type_id):
                filtered_id = line[1]
                break
        return filtered_id in groups_and_types or str(poi_type_id) in groups_and_types
        
    return list(filter(group_or_type_filter, poi_list))