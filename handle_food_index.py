index_ranges = [
    {"index_range": (0, 5), "quality_type": 'bad'},
    {"index_range": (5, 10), "quality_type": 'medium'},
    {"index_range": (10, 15), "quality_type": 'good'},
]

def handle_food_index(food_index):
    is_find_range = False
    for index in index_ranges:
        index_range = index["index_range"] 
        if index_range[0] <= food_index < index_range[1]:
            is_find_range = True
            return index["quality_type"]
    if not is_find_range:
        return 'good'