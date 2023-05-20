import json
from data_gathering.fetch_newsdata import format_newsdata_url
from data_gathering.fetch_cryptopanic import format_cryptopanic_url
from data_gathering.fetch_news_api import fetch_news_api
from data_gathering.fetch_api import fetch_api
from data_gathering.fetch_googlenews import fetch_googlenews
from data_parsing.response_parsing import ParseApiResponse

def store_news_response(news_reponse, source):
    json_news_outputs = json.dumps(news_reponse, indent=4)

    with open(f"data/{source}.json", "w") as outfile:
        outfile.write(json_news_outputs)


def generate_news_overview():
    response_parser = ParseApiResponse()
    news_apis = {
        'cryptopanic': (format_cryptopanic_url, {}),
        'newsdata': (format_newsdata_url, {}),
        'news_api': (fetch_news_api, {}),
        'google_api': (fetch_googlenews, {})
        
    }

    news_outputs = {key: {} for key, _ in news_apis.items()}

    # collect api inputs
    for api_name, (url_formatter, url_settings) in news_apis.items():

        # news api is a python package that doesn't require the response fetching
        if api_name == 'news_api':
            api_response = fetch_news_api()
        elif api_name == 'google_api':
            api_response == fetch_googlenews()
        else:
            api_response = fetch_api(url_formatter, url_settings)

        # parse the API response to be harmonised with the rest
        parsed_api_response = response_parser.parse_api_response(api_response, api_name)

        # store individual response
        store_news_response(parsed_api_response, api_name)

        news_outputs[api_name] = parsed_api_response

    # store the full out
    store_news_response(news_outputs, 'combined')


if __name__ == '__main__':
    generate_news_overview()