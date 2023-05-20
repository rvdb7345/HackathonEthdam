import requests
import json
import our_secrets

def format_newsdata_url():
    """Handle of URL variables for API POST."""
    url = f'https://newsdata.io/api/1/news?apikey={our_secrets.newsdata_api}&q=cryptocurrency'

    return url


