#  File for selecting charts from dune
import pandas as pd


def get_topics_from_articles(articles):
    # Selects 5 most relevant topics based on articles
    pass


def get_charts(relevant_topics, chart_topics="charts_topics.csv"):
    # Selects charts based on given topics
    charts_topics_df = pd.read_csv(chart_topics)

    set1 = set(relevant_topics)
    # Iterate over the rows of the dataframe
    for index, row in charts_topics_df.iterrows():
        set2 = set(row["topics"])
        common_elements = set1.intersection(set2)
        if len(common_elements) == 0:
            # Drop the row if the 'City' column value is 'London'
            charts_topics_df = charts_topics_df.drop(index)
    return charts_topics_df


def create_chart_file(selected_charts):
    # Outputs a text file to be merged into the final final text file

    # Open a file in write mode
    with open("final_charts.txt", "a") as file:
        # Write content to the file
        file.write("## Relevant graphs of the week\n")
        for i, chart in enumerate(selected_charts):
            file.write("Graph {}: {}".format(i, chart["name"]))
            file.wirte(str(chart["link"]))


get_charts([1, 2, 3])
