import requests
import json
import secrets

def make_url(filter=None, currencies=None, kind=None, region=None, page=None):
    """Handle of URL variables for API POST."""
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token={}'.format(secrets.cryptopanic_api)

    if currencies is not None:
        if len(currencies.split(',')) <= 50:
            url += "&currencies={}".format(currencies)
        else:
            print("Warning: Max Currencies is 50")
            return

    if kind is not None and kind in ['news', 'media']:
        url += "&kind={}".format(kind)

    filters = ['rising', 'hot', 'bullish', 'bearish', 'important', 'saved', 'lol']
    if filter is not None and filter in filters:
        url += "&filter={}".format(filter)

    regions = ['en', 'de', 'es', 'fr', 'it', 'pt', 'ru']  # (English), (Deutsch), (Español), (Français), (Italiano), (Português), (Русский)--> Respectively
    if region is not None and region in regions:
        url += "&region={}".format(region)

    if page is not None:
        url += "&page={}".format(page)

    return url


def get_data_from_api():
    # The URL of the API endpoint
    url = make_url(filter=None, currencies=None, kind=None, region=None, page=None)

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()

        # Print the data
        parsed_response = json.dumps(data, indent=4)
        print(parsed_response)
    else:
        print(f'Request failed with status code {response.status_code}')

    return parsed_response

def store_news_response(news_reponse):
    with open("data/cryptopanic.json", "w") as outfile:
        outfile.write(news_reponse)

if __name__ == "__main__":
    news_response = get_data_from_api()
    store_news_response(news_response)


