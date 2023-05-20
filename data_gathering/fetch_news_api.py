
from newsapi import NewsApiClient
from typing import Dict
from datetime import datetime, timedelta
import our_secrets

def fetch_news_api()->Dict:
    """Fect data from newsapi."""
    newsapi = NewsApiClient(api_key=our_secrets.news_api)
    sources = ['coindesk.com', 'cointelegraph.com']
    data=[]
    
    # Get today's date
    today = datetime.today().date()

    # Calculate the date one month ago
    one_month_ago = today - timedelta(days=30)

    # Format the date as 'YYYY-MM-DD'
    one_month_ago_date = one_month_ago.strftime('%Y-%m-%d')
    today_date = today.strftime('%Y-%m-%d')
    
    for source in sources:
        all_articles = newsapi.get_everything(
                                            domains=source,
                                            from_param=one_month_ago_date,
                                            to=today_date,
                                            language='en',
                                            sort_by='relevancy',
                                            page=3)
        data.extend(all_articles)
    return data

if __name__=='__main__':
    results=fetch_news_api()
    print(results)