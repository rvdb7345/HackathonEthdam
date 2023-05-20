from data_parsing.json_parsing import convert_json_to_rds

if __name__ == '__main__':
    formatted_news = convert_json_to_rds('data/20230520_combined.json')
    print(formatted_news)