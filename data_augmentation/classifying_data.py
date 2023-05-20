
import pandas as pd
import datetime

def grouping_news_article_per_week(df:pd.DataFrame):
    df['date_column'] = pd.to_datetime(df['published_at'], format='%Y%m%d%H%M%S')
    # Sort the DataFrame by date
    today = max(df['date_column'])
    cutoff_date =today - datetime.timedelta(days=7)
    return df[df['date_column'] > cutoff_date].sort_values('date_column')



if __name__=='__main__':
    df = pd.read_json('data/20230520_combined.json', convert_dates=False)
    grouping_news_article_per_week(df)