import pandas as pd


def check_matching_word(row, tickers_list:pd.DataFrame):
    label=[]
    for index, ticker in tickers_list.iterrows():
        try:
            if ticker['symbol'] in row['content'] or ticker['name'] in row['content']:
                label.append(ticker['symbol'])
        except:
            if ticker['symbol'] in row['title'] or ticker['name'] in row['title']:
                label.append(ticker['symbol'])
    return label

def label_data(df:pd.DataFrame,labels:pd.DataFrame):
    """Attributes a ticker to a newspaper."""
    df['tickers'] = df.apply(lambda row: check_matching_word(row, labels), axis=1)

    
    
    
if __name__=='__main__':
    df = pd.read_json('data/20230520_combined.json', convert_dates=False)
    labels = pd.read_csv('data/tickers.csv')
    label_data(df,labels)