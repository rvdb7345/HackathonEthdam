"""
Main file to be run every monday morning. Performs all the steps necessary to 
create the newsletter.
"""

# Imports
from create_news_selection import select_representative_documents
from data_parsing.json_parsing import convert_json_to_markdown, convert_json_to_rds
from json_to_markdown import article_json_to_markdown
from generate_news_overview import generate_news_overview
from data_augmentation.classifying_data import grouping_news_article_per_week
from create_visual.create_cointable_image import create_cointable_image
from datetime import datetime
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

    def select_articles(self, news_last_week):
        forbidden_subjects = ["best_crypto", "best_2023"]

        articles_to_publish = select_representative_documents(
            news_last_week,
            forbidden_subjects=forbidden_subjects,
            num_articles_to_publish=10,
            plot_clusters=False,
        )
        print(articles_to_publish)
        return articles_to_publish

    def gather_high_metrics(self):
        # Gather the high level metrics
        create_cointable_image()

    def format_data(self, df: pd.DataFrame) -> None:
        # Turn the gathered data to a nice format
        markdown_json = convert_json_to_markdown(df)
        article_json_to_markdown(markdown_json)

    # Gather the dune charts
    pass

    def create_final_output(self):
        # Create the output text file to be copied into Mirror
        pass

    def weekly_update(self, gather_new_metrics=True):
        # Function to do a full run, to be executed weekly
        if gather_new_metrics:
            all_articles_df = self.gather_article_data()
            selected_articles_df = self.select_articles(all_articles_df)
            self.gather_high_metrics()
            self.gather_dune_charts()

        self.format_data()

        self.create_final_output()


if __name__ == "__main__":
    crypchro = CryptoChronicles()
    crypchro.gather_article_data()
