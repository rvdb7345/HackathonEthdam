import datetime
from fetch_api import fetch_api
import csv


def fetch_coingecko():
    coins = {}
    current_date = datetime.date.today()
    week_ago_date = (current_date - datetime.timedelta(days=7)).strftime("%d-%m-%Y")

    current_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&locale=en"

    current_data = fetch_api(current_url, url_settings=None)
    for i in current_data:
        try:
            coin_id = i["id"]
            current_price = i["current_price"]
            coins[coin_id] = {"current_price": current_price}
        except Exception as e:
            print(str(i) + " " + str(e))

    for coin in coins.keys():
        try:
            data = fetch_api(
                f"https://api.coingecko.com/api/v3/coins/{coin}/history?date={week_ago_date}",
            )
            if (
                data is not None
                and "market_data" in data
                and "current_price" in data["market_data"]
                and "usd" in data["market_data"]["current_price"]
            ):
                coins[coin].update(
                    {"history_price": data["market_data"]["current_price"]["usd"]}
                )
        except Exception as e:
            print(f"Error fetching data for {coin}: {str(e)}")

    return coins


if __name__ == "__main__":
    results = fetch_coingecko()
    csv_file = "data/top10coins_data.csv"
    # Open the CSV file in write mode
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

          # Write the header row
        writer.writerow(['Cryptocurrency', 'Current Price', 'Last weeks Price', 'Percentage Change'])

        # Write each row of data
        for crypto, info in results.items():
            current_price = info['current_price']
            history_price = info['history_price']
            percentage_change = ((current_price - history_price) / history_price) * 100
            writer.writerow([crypto, current_price, round(history_price, 2), round(percentage_change, 2)])
            # insert date and append weekly data

    print("Data has been written to ", csv_file)