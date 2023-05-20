import requests
import json
import secrets

def format_newsdata_url():
    """Handle of URL variables for API POST."""
    url = f'https://newsdata.io/api/1/news?apikey={secrets.newsdata_api}&q=cryptocurrency'

    return url


