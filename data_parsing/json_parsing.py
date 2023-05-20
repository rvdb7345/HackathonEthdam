import json
import pandas as pd

def convert_json_to_rds(json_data):
    rds_news = pd.read_json(json_data, convert_dates=False)

    return rds_news

def convert_json_to_markdown(json_data,convert_dates=False):
    """Convert data to markdown format for beau."""
    if isinstance(json_data,pd.DataFrame):
        rds_news = json_data
    elif isinstance(json_data,str):
        rds_news = convert_json_to_rds(json_data)
        
    rds_news.columns = rds_news.columns.str.replace('link', 'hyperlink')
    return rds_news[['title','hyperlink','keywords','content']].sample(n=10)


