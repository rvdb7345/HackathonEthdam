import json
import pandas as pd

def convert_json_to_rds(json_data):
    rds_news = pd.read_json(json_data, convert_dates=False)

    return rds_news


