"""
Main file to be run every monday morning. Performs all the steps necessary to 
create the newsletter.
"""

# Imports
from data_parsing.json_parsing import convert_to_markdown


def main():
    # Gather the high level metrics
    pass

    # Gather the newsdata
    markdown_json = convert_to_markdown('data/20230520_combined.json')

    # Gather the dune chart
    pass

    # Create the output text file to be copied into Mirror
    pass


if __name__ == '__main__':
    main()                                                                      