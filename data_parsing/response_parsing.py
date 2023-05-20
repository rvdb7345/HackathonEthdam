from datetime import datetime


class ParseApiResponse():
    def __init__(self):
        pass

    def parse_api_response(self, response, source):
        if source == 'cryptopanic':
            parsed_response = self.parse_cryptopanic(response)
        elif source == 'newsdata':
            parsed_response = self.parse_newsdata(response)
        elif source == 'news_api':
            parsed_response = self.parse_news_api(response)
        elif source == 'google_api':
            parsed_response = self.parse_google_news_api(response)
            
        else:
            assert False, f'Source not recognised: {source}'

        return parsed_response

    def parse_cryptopanic(self, response):
        parsed_results = []

        for news_article in response:
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
        parsed_results = []

        for news_article in response:
            news_result = {}
            news_result['kind'] = 'news'
            news_result['publisher_domain'] = news_article['link']
            news_result['publisher'] = news_article['source_id']

            news_result['keywords'] = news_article['keywords']
            news_result['author'] = news_article['creator']

            news_result['title'] = news_article['title']
            news_result['abstract'] = news_article['description']
            news_result['content'] = news_article['content']
            news_result['published_at'] = \
                datetime.strptime(news_article['pubDate'], '%Y-%m-%d %H:%M:%S').strftime("%Y%m%d%H%M%S")
            news_result['language'] = news_article['language']

            parsed_results.append(news_result)

        return parsed_results

    def parse_news_api(self, response):
        return response
    
    def parse_google_news_api(self, response):
        return response




