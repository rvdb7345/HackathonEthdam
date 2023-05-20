import datetime
import requests


def fetch_coingecko():
  coins = []
  current_date = datetime.date.today()
  week_ago_date = current_date - datetime.timedelta(days=7)

  current_url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en' 

  current_data = read_api(current_url)
  for i in current_data[:10]:
    id = i['id']
    current_price = i['current_price']
    coins[id] = {'current_price' : current_price}

  for coin in coins.keys():
    data = read_api(f'https://api.coingecko.com/api/v3/coins/{coin}/history?date={week_ago_date}')
    coins[coin].update({'history_price': data['market_data']['current_price']['usd']})

  return coins

if __name__ == "__main__":
  results = fetch_coingecko()
  print(results)