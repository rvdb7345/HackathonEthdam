from datetime import datetime


class ParseApiResponse():
    def __init__(self):
        pass

    def parse_api_response(self, response, source):
        if source == 'cryptopanic':
            parsed_response = self.parse_cryptopanic(response)
        elif source == 'newsdata':
            parsed_response = self.parse_newsdata(response)
        else:
            assert False, f'Source not recognised: {source}'

        return parsed_response

    def parse_cryptopanic(self, response):
        parsed_results = []

        print(type(response))

        for news_article in response['results']:
            news_result = {}
            news_result['kind'] = news_article['kind']
            news_result['publisher_domain'] = news_article['domain']
            news_result['title'] = news_article['title']
            news_result['published_at'] = \
                datetime.strptime(news_article['published_at'], '%Y-%m-%dT%H:%M:%SZ').strftime("%Y%m%d%H%M%S")

            news_result['api_url'] = news_article['url']

            if news_article.get('currencies', None) is not None:
                news_result['currency_codes'] = [currency['code'] for currency in news_article['currencies']]
            if news_article.get('source', None) is not None:
                news_result['language'] = news_article['source']['region']

            parsed_results.append(news_result)

        return parsed_results

    def parse_newsdata(self, response):
        return response



