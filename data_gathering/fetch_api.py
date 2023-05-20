import requests
import json


def fetch_api(url, url_settings):
    # The URL of the API endpoint
    # Send a GET request to the API endpoint
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()

        # Print the data
        print(data)
    else:
        print(f'Request failed with status code {response.status_code}')

    return data
