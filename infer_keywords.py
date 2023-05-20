import pandas as pd
from data_augmentation.keyword_extraction import KeywordGenerator

if __name__ == '__main__':
    keyword_generator = KeywordGenerator()

    formatted_news = pd.read_csv('data/20230520_combined.csv', engine='python')
    formatted_news.dropna(subset=['content'], inplace=True)

    print(formatted_news.iloc[0]['content'])
    keywords = keyword_generator.create_keywords_for_doc(formatted_news.iloc[0]['content'])
    print(keywords)
