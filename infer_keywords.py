import pandas as pd
from tqdm import tqdm
from data_augmentation.keyword_extraction import KeywordGenerator

if __name__ == '__main__':
    keyword_generator = KeywordGenerator()
    formatted_news = pd.read_csv('data/20230520_combined.csv', engine='python')

    for idx, row in tqdm(formatted_news.iterrows(), total=len(formatted_news)):
        if not pd.isna(row['content']):
            keywords = keyword_generator.create_keywords_for_doc(row['content'])
            formatted_news.loc[idx, 'algorithmic_keywords'] = str([keyword[0] for keyword in keywords])

    formatted_news.to_csv('data/20230520_combined_keywords.csv')



