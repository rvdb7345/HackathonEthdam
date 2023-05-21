import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import pandas as pd

import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import umap
import matplotlib.pyplot as plt


def select_representative_documents(documents, num_clusters=3, num_representatives=1):
    # Load pre-trained language model for text embedding
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Embed the documents
    document_embeddings = model.encode(documents)

    # Perform dimensionality reduction using UMAP
    reducer = umap.UMAP()
    reduced_embeddings = reducer.fit_transform(document_embeddings)

    # Cluster the reduced embeddings
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(reduced_embeddings)

    # Select representative documents from each cluster
    selected_documents = []
    for cluster_id in range(num_clusters):
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        cluster_embeddings = document_embeddings[cluster_indices]

        # Find the indices of the representative documents
        representative_indices = np.argpartition(
            np.linalg.norm(cluster_embeddings - np.mean(cluster_embeddings, axis=0), axis=1),
            num_representatives
        )[:num_representatives]

        # Append the representative documents to the selected documents list
        selected_documents.extend([documents[cluster_indices[idx]] for idx in representative_indices])

    # Plot the UMAP visualization
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=cluster_labels, cmap='viridis')
    plt.title('UMAP Visualization of Document Embeddings')
    plt.show()

    return selected_documents


