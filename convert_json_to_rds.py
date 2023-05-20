from data_parsing.json_parsing import convert_json_to_rds

if __name__ == '__main__':
    formatted_news = convert_json_to_rds('data/20230520_combined.json')

    formatted_news.to_csv('data/20230520_combined.csv')
    print(formatted_news.info())