from bertopic import BERTopic

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP

import matplotlib
import matplotlib.pyplot as plt

def visualise_topics(model, docs, topics):
    # Prepare data for plotting
    embeddings = model._extract_embeddings(docs, method="document")
    umap_model = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit(embeddings)
    df = pd.DataFrame(umap_model.embedding_, columns=["x", "y"])
    df["topic"] = topics

    # Plot parameters
    top_n = 10
    fontsize = 12

    # Slice data
    to_plot = df.copy()
    to_plot[df.topic >= top_n] = -1
    outliers = to_plot.loc[to_plot.topic == -1]
    non_outliers = to_plot.loc[to_plot.topic != -1]

    # Visualize topics
    cmap = matplotlib.colors.ListedColormap(['#FF5722',  # Red
                                             '#03A9F4',  # Blue
                                             '#4CAF50',  # Green
                                             '#80CBC4',  # FFEB3B
                                             '#673AB7',  # Purple
                                             '#795548',  # Brown
                                             '#E91E63',  # Pink
                                             '#212121',  # Black
                                             '#00BCD4',  # Light Blue
                                             '#CDDC39',  # Yellow/Red
                                             '#AED581',  # Light Green
                                             '#FFE082',  # Light Orange
                                             '#BCAAA4',  # Light Brown
                                             '#B39DDB',  # Light Purple
                                             '#F48FB1',  # Light Pink
                                             ])

    # Visualize outliers + inliers
    fig, ax = plt.subplots(figsize=(15, 15))
    scatter_outliers = ax.scatter(outliers['x'], outliers['y'], c="#E0E0E0", s=1, alpha=.3)
    scatter = ax.scatter(non_outliers['x'], non_outliers['y'], c=non_outliers['topic'], s=1, alpha=.3, cmap=cmap)

    # Add topic names to clusters
    centroids = to_plot.groupby("topic").mean().reset_index().iloc[1:]
    for row in centroids.iterrows():
        topic = int(row[1].topic)
        text = f"{topic}: " + "_".join([x[0] for x in model.get_topic(topic)[:3]])
        ax.text(row[1].x, row[1].y * 1.01, text, fontsize=fontsize, horizontalalignment='center')

    ax.text(0.99, 0.01, f"BERTopic - Top {top_n} topics", transform=ax.transAxes, horizontalalignment="right",
            color="black")
    plt.xticks([], [])
    plt.yticks([], [])
    plt.savefig("BERTopic_Example_Cluster_Plot.png")
    plt.show()


def get_topics_out(docs, plot=False):
    vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english")
    model = BERTopic(vectorizer_model=vectorizer_model)
    topics, probs = model.fit_transform(docs)

    print(model.get_topic_freq())
    print(model.get_topic_info())

    if plot:
        visualise_topics(model, docs, topics)

    representative_docs = model.get_representative_docs()

    return representative_docs, model.get_topic_info()['Name'].to_list()

