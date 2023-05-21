"""
Main file to be run every monday morning. Performs all the steps necessary to 
create the newsletter.
"""

# Imports
from data_parsing.json_parsing import convert_json_to_markdown,convert_json_to_rds
from json_to_markdown import article_json_to_markdown
from generate_news_overview import generate_news_overview
from data_augmentation.classifying_data import grouping_news_article_per_week
from  datetime import datetime
import pandas as pd

class CryptoChronicles:
    def __init__(self):
        pass

    def gather_article_data(self):
        # Function to create a new dataset by calling API's
        now = datetime.now().strftime("%Y%m%d")  # current date and time
        aggregated_news = generate_news_overview(now)
        # Get the data as rds and filter english language only
        df = pd.DataFrame(aggregated_news)
        # return the last 7 days
        df = grouping_news_article_per_week(df)
        return df

    def gather_high_metrics(self):
        # Gather the high level metrics
        pass

    def format_data(self,df:pd.DataFrame)->None:
        # Turn the gathered data to a nice format
        markdown_json = convert_json_to_markdown(df)
        article_json_to_markdown(markdown_json)

    def gather_dune_charts(self):
        # Gather the dune charts
        pass

    def create_final_output(self):
        # Create the output text file to be copied into Mirror
        pass

    def weekly_update(self, gather_new_metrics=True):
        # Function to do a full run, to be executed weekly
        if gather_new_metrics:
            self.gather_article_data()
            self.gather_high_metrics()
            self.gather_dune_charts()

        self.format_data()
        self.create_final_output()


if __name__ == "__main__":
    crypchro = CryptoChronicles()
    crypchro.gather_article_data()
