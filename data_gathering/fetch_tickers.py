import datetime

import pandas as pd

from fetch_api import fetch_api

def fetch_tickers():
    current_date = datetime.date.today()
    current_url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=200&page=1&sparkline=false&locale=en'

    current_data = fetch_api(current_url, url_settings=None)

    coin_names = pd.DataFrame(columns=['name', 'symbol'], index=list(range(200)))
    for idx, coin_info in enumerate(current_data):
        coin_names.loc[idx, :] = [coin_info['name'], coin_info['symbol']]

    return coin_names


if __name__ == "__main__":
    results = fetch_tickers()
    results.to_csv('../data/tickers.csv')
    print(results)
