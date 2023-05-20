import requests
import json
import time


def fetch_api(url, url_settings=None, recursive_check=False):
    # The URL of the API endpoint
    # Send a GET request to the API endpoint
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()
    elif response.status_code == 429:
        if not recursive_check:
            # Wait for the API to cool down
            print("Waiting because the gecko is sleeping....")
            time.sleep(70)
            data = fetch_api(url, recursive_check=True)
        else:
            print("Gecko keeps sleeping, ABORTING.")
            return False
    else:
        print(f"Request failed with status code {response.status_code}")

    return data
