import json
import pandas as pd

def load_all_news(file_path):

    # Opening JSON file
    with open(file_path) as f:

        # returns JSON object as
        # a dictionary
        data = json.load(f)

    return data

def convert_json_to_rds(json_data):
    rds_news = pd.read_json(json_data)

    return rds_news


