import json
from data_gathering.fetch_newsdata import format_newsdata_url
from data_gathering.fetch_cryptopanic import format_cryptopanic_url
from data_gathering.fetch_api import fetch_api
from data_parsing.response_parsing import ParseApiResponse

def store_news_response(news_reponse, source):
    with open(f"data/{source}.json", "w") as outfile:
        outfile.write(news_reponse)


def generate_news_overview():
    response_parser = ParseApiResponse()
    news_apis = {
        'cryptopanic': (format_cryptopanic_url, {}),
        'newsdata': (format_newsdata_url, {})
    }

    news_outputs = {key: {} for key, _ in news_apis.items()}

    # collect api inputs
    for api_name, (url_formatter, url_settings) in news_apis.items():
        api_response = fetch_api(url_formatter, url_settings)
        parsed_api_response = response_parser.parse_api_response(api_response, api_name)

        # store individual response
        store_news_response(parsed_api_response, api_name)

        news_outputs[api_name] = parsed_api_response

    json_news_outputs = json.dumps(news_outputs, indent=4)

    store_news_response(json_news_outputs, 'combined')

if __name__ == '__main__':
    generate_news_overview()