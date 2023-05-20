import requests
import json

def get_data_from_api():
    # The URL of the API endpoint
    url = 'https://api.example.com/data'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()

        # Print the data
        print(json.dumps(data, indent=4))
    else:
        print(f'Request failed with status code {response.status_code}')

if __name__ == "__main__":
    get_data_from_api()
