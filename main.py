"""
Main file to be run every monday morning. Performs all the steps necessary to 
create the newsletter.
"""

# Imports
from data_parsing.json_parsing import convert_json_to_markdown
from json_to_markdown import article_json_to_markdown


class CryptoChronicles:
    def init(self):
        pass

    def gather_article_data(self):
        # Function to create a new dataset by calling API's
        pass

    def gather_high_metrics(self):
        # Gather the high level metrics
        pass

    def format_data(self):
        # Turn the gathered data to a nice format
        markdown_json = convert_json_to_markdown("data/20230520_combined.json")
        article_json_to_markdown(markdown_json)

    def gather_dune_charts(self):
        # Gather the dune charts
        pass

    def create_final_output(self):
        # Create the output text file to be copied into Mirror
        pass


# if __name__ == "__main__":
#     main()
